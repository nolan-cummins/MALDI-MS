from ui.mainwindow import * # main Qt core imports
from PySide6.QtCore import Qt, QTimer, Signal, QByteArray, Slot, QIODevice, QThread
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QComboBox, QStyleFactory
from PySide6.QtGui import QIcon, QAction, QCloseEvent, QImage, QPixmap
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo 

import ctypes 
from ctypes import wintypes
myappid = 'int.maldi' 
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# utils
from pathlib import Path
from time import time, sleep, perf_counter
import sys
from utils import FluigentController, ArduinoController, enable_layout, scriptRunner, textBackground
import pandas as pd
import json
from video_loader import processVideo
import cv2
import numpy as np
import pypylon.pylon as py
from camera import captureCamera, videoSaver
from model import runModel
from watchdog import DeviceWatchdog, DeviceState
from session_logger import SessionLogger

# windows-specific constants to capture USB device connection/disconnection
WM_DEVICECHANGE = 0x0219
DBT_DEVICEARRIVAL = 0x8000 
DBT_DEVTYP_DEVICEINTERFACE = 0x0005
DEVICE_NOTIFY_WINDOW_HANDLE = 0x00000000

class GUID(ctypes.Structure):
    _fields_ = [
        ('Data1', ctypes.c_ulong),
        ('Data2', ctypes.c_ushort),
        ('Data3', ctypes.c_ushort),
        ('Data4', ctypes.c_ubyte * 8)
    ]

GUID_DEVINTERFACE_USB_DEVICE = GUID(0xA5DCBF10, 0x6530, 0x11D2, (ctypes.c_ubyte * 8)(0x90, 0x1F, 0x00, 0xC0, 0x4F, 0xB9, 0x51, 0xED))

class DEV_BROADCAST_DEVICEINTERFACE_W(ctypes.Structure):
    _fields_ = [
        ('dbcc_size', wintypes.DWORD),
        ('dbcc_devicetype', wintypes.DWORD),
        ('dbcc_reserved', wintypes.DWORD),
        ('dbcc_classguid', GUID),
        ('dbcc_name', wintypes.WCHAR * 1)
    ]

# imported PySide6 .ui main window class, see ./ui/mainwindow.py

class MainWindow(QMainWindow, Ui_MainWindow): 
    send_script_signal = Signal(list)
    
    #mask_frame_out = Signal(object) 
    start_mask_record = Signal(str, int, tuple, bool, bool)
    release_mask_writer = Signal()

    def __init__(self):
        super(MainWindow, self).__init__() 
        self.setupUi(self)

        print(f'Running...\n')  
        icon = QIcon('assets/icon/icon.ico')
        self.setWindowIcon(icon)
        QApplication.setWindowIcon(icon)
        self.setWindowTitle("MALDI Control Suite")

        # connect scrollbars & spinboxes
        self._init_scrollbar_inputs()

        # camera controls
        enable_layout(self.camera_controls_layout, False)
        enable_layout(self.recording_layout, False)
        self.captureCamera = None 
        self.tlf = py.TlFactory.GetInstance()
        self.camera_frame.setStyle(QStyleFactory.create("Fusion"))
        self.last_frame_time_disp = perf_counter()
        self.last_timestamp = perf_counter()
        self.actual_fps = 0.0

        # connect mouse signals
        self.is_key_C_pressed = False
        self.is_drawing_crop = False
        self.crop_start = None
        self.crop_end = None
        self.final_crop = None 
        
        # Connect mouse signals
        self.camera_label.mousePressed.connect(self.on_mouse_press)
        self.camera_label.mouseMoved.connect(self.on_mouse_move)
        self.camera_label.mouseReleased.connect(self.on_mouse_release)

        # pump controls
        self._init_pump_controls()

        # video controls
        self.videoLoader = None
        self.actionOpen_Video = QAction("Open Video", self)
        self.menuFile.addAction(self.actionOpen_Video)
        self.actionOpen_Video.triggered.connect(self.open_video) # type: ignore
        self.camera_frame.setFocusPolicy(Qt.NoFocus) # type: ignore
        self.video_paused = False
        self.show_overlay = True
        self.camera_label.setFocusPolicy(Qt.StrongFocus)
        self.camera_label.setFocus(Qt.OtherFocusReason)

        # Initialize background mask saver identical to the camera logic
        self.mask_saver_thread = QThread()
        self.mask_saver = videoSaver()
        self.mask_saver.moveToThread(self.mask_saver_thread)
        self.mask_saver_thread.start()
        
        # Connect strictly typed signals
        #self.mask_frame_out.connect(self.mask_saver.saveFrame)
        self.start_mask_record.connect(self.mask_saver.startWriter)
        self.release_mask_writer.connect(self.mask_saver.releaseWriter)

        self.current_pressures = [0.0, 0.0]
        
        # recording controls
        self.record_button.clicked.connect(self.toggle_recording) 
        self.screenshot_button.clicked.connect(self.take_screenshot)
        self.is_recording = False
        self.save_path = str(Path.cwd())

        # data dictionary for recording
        self.data = {
            "timestamps": [], "p1_measured": [], "p2_measured": [], "p1_setpoint": [], "p2_setpoint": [],
            "x": [], "y": [], "z": [], "x_setpoint": [], "y_setpoint": [], "z_setpoint": [],
            "arduino_time": [], "box_x1": [], "box_y1": [], "box_x2": [], "box_y2": [], "box_conf": [],
            "volume_pl": [], "volume_px3": []
        }
        self.start_time = perf_counter()

        # stage/arduino controls
        enable_layout(self.stage_layout, False)
        self._init_stage_controls()
        self._init_stage_limits()
        self.px_per_step = 1062/300 # 1062 pixels across 300 step movement

        # menubar
        self._init_menubar()

        # timers
        self.pump_timer = QTimer()
        self.pump_timer.timeout.connect(self.update_pump_info) # type: ignore
        self.pump_timer.start(33)

        self.stage_move_timer = QTimer(self)
        self.stage_move_timer.timeout.connect(self._handle_continuous_stage_move) # type: ignore
        self.stage_move_timer.setInterval(33) 

        # pump controller logic
        self.pumps_found = False
        self.controller = FluigentController()
        self.script_runner = scriptRunner(self)
        self.script_runner.feed_signal.connect(self.feedframes_chkbox.setChecked)
        self.script_runner.stage_signal.connect(self._handle_script_stage_command)
        
        # Watchdog and Session Logger
        self.watchdog = DeviceWatchdog(self)
        self.session_logger = SessionLogger()
        self.watchdog.device_state_changed.connect(self._on_device_state_changed)
        self.watchdog.critical_failure.connect(self._on_critical_failure)
        self.watchdog.start_monitoring()
        
        # Register devices (callbacks updated when threads are created)
        self.watchdog.register_device("camera", expected_hz=100)
        self.watchdog.register_device("fluigent", expected_hz=30)
        self.watchdog.register_device("arduino", expected_hz=30)
        self.watchdog.register_device("model", expected_hz=60)
        self.send_script_signal.connect(self.script_runner.runScript)
        self.script_runner.pump_signal.connect(self.controller.set_pressure)
        self.run_script_button.clicked.connect(self.run_script) # type: ignore
        
        self.stop_script_button.clicked.connect(lambda: self.script_runner.stop_script())

        # yolo model controls
        self._init_model_controls()
        self.latest_boxes = []
        self.latest_masks = []
        self.latest_scores = []

        # usb
        self.detect_instruments() # type: ignore
        self._register_for_usb_notifications() # type: ignore

    def _init_model_controls(self):
        # Initialize scrollbars and spinboxes synchronization
        self.yolo_scroll_inputs = {
            "confidence": (self.confidence_scrollbar, self.confidence_spbx),
            "max_detections": (self.max_detections_scrollbar, self.max_detections_spbx),
            "clip_limit": (self.clip_limit_scrollbar, self.clip_limit_spbx),
            "tile_grid": (self.tile_grid_scrollbar, self.tile_grid_spbx)
        }
        
        for (scrollbar, spinbox) in self.yolo_scroll_inputs.values():
            scrollbar.valueChanged.connect(spinbox.setValue)
            spinbox.valueChanged.connect(scrollbar.setValue)

        self.model_thread = None
        self.run_model_btn.setCheckable(True) 
        self.run_model_btn.toggled.connect(self.toggle_model)
        self.stop_model_btn.clicked.connect(self.stop_model)
        self.stop_model_btn.clicked.connect(lambda: self.run_model_btn.setChecked(False))

        self.clip_limit_spbx.valueChanged.connect(self.update_clahe_settings)
        self.tile_grid_spbx.valueChanged.connect(self.update_clahe_settings)
        self.clahe_checkbox.toggled.connect(self.toggle_clahe)

        self.confidence_scrollbar.valueChanged.connect(
            lambda v: self.model_worker.updateConfidence(v / 100.0) if getattr(self, 'model_worker', None) else None
        )

    @Slot(str, float)
    def _handle_script_stage_command(self, cmd_type, value):
        """Routes commands from the scriptRunner to the appropriate hardware methods."""
        try:
            # Split e.g., 'move_x' into ['move', 'x']
            prefix, axis = cmd_type.split("_")
            
            if prefix == "move":
                # Uses your existing relative movement logic + UI update
                self._stage_move_rel(axis, value)
            elif prefix == "speed":
                # Updates the spinbox and sends 'A' command to Arduino
                self._stage_apply_kinematics(axis, speed=value)
            elif prefix == "accel":
                # Updates the spinbox and sends 'A' command to Arduino
                self._stage_apply_kinematics(axis, accel=value)
                
        except Exception as e:
            print(f"Error handling script stage command: {e}")

    def map_to_image_coords(self, mx, my):
        """Maps UI label coordinates back to the original image dimensions."""
        if not hasattr(self, 'p_shape') or not hasattr(self, 'latest_frame_shape'): return None
        pix_w, pix_h = self.p_shape
        img_h, img_w = self.latest_frame_shape[:2]
        lbl_w, lbl_h = self.camera_label.width(), self.camera_label.height()

        x_off = (lbl_w - pix_w) / 2
        y_off = (lbl_h - pix_h) / 2

        ix = int((mx - x_off) * (img_w / pix_w))
        iy = int((my - y_off) * (img_h / pix_h))
        return max(0, min(img_w, ix)), max(0, min(img_h, iy))

    #@Slot(tuple)
    def on_mouse_press(self, pos):
        if self.is_key_C_pressed:
            self.camera_label.setFocus()
            img_pos = self.map_to_image_coords(*pos)
            if img_pos:
                self.crop_start = img_pos
                self.crop_end = img_pos
                self.is_drawing_crop = True

    #@Slot(tuple)
    def on_mouse_move(self, pos):
        if self.is_drawing_crop and self.is_key_C_pressed:
            img_pos = self.map_to_image_coords(*pos)
            if img_pos:
                self.crop_end = img_pos

    #@Slot(tuple)
    def on_mouse_release(self, pos):
        if self.is_drawing_crop:
            self.is_drawing_crop = False
            if self.crop_start and self.crop_end:
                x1, x2 = sorted([self.crop_start[0], self.crop_end[0]])
                y1, y2 = sorted([self.crop_start[1], self.crop_end[1]])
                if x2 > x1 and y2 > y1: # Ensure valid box
                    self.final_crop = (x1, y1, x2, y2)
                    self.update_model_crop()

    def toggle_clahe(self, checked):
        if getattr(self, 'model_worker', None):
            self.model_worker.setClaheEnabled(checked)
        if hasattr(self, 'video_converter') and self.video_converter:
            self.video_converter.setClaheEnabled(checked)

    def update_clahe_settings(self):
        clip = float(self.clip_limit_spbx.value())
        tile = int(self.tile_grid_spbx.value())
        if getattr(self, 'model_worker', None):
            self.model_worker.updateClaheParams(clip, tile)
        if hasattr(self, 'video_converter') and self.video_converter:
            self.video_converter.updateClaheParams(clip, tile)

    def stop_model(self):
        if getattr(self, 'model_worker', None):
            self.model_worker.stop()
        if self.model_thread:
            self.model_thread.quit()
            self.model_thread.wait()
            self.model_thread = None

    @Slot(bool)
    def toggle_model(self, checked):
        if checked:
            self.start_model()
        else:
            self.stop_model()

    def start_model(self):
        model_path = self.model_combobox.currentText()
        if not model_path:
            print("No model selected!")
            self.run_model_btn.setChecked(False)
            return

        if self.model_thread:
            self.stop_model()

        print(f"Starting model: {model_path}")
        self.model_thread = QThread()
        self.model_worker = runModel(model_path)
        self.model_worker.moveToThread(self.model_thread)

        # Watchdog reference
        self.model_worker.watchdog = self.watchdog
        self.watchdog.register_device("model", expected_hz=60,
                                      reconnect_callback=self.start_model)

        self.ema_chckbx.toggled.connect(self.model_worker.setEmaEnabled)
        self.model_worker.setEmaEnabled(self.ema_chckbx.isChecked())
        self.fit_ellipse_chbx.toggled.connect(self.model_worker.setFitEllipseEnabled)
        
        # Send initial confidence
        self.model_worker.updateConfidence(self.confidence_scrollbar.value() / 100.0)
        self.feedframes_chkbox.toggled.connect(lambda checked: self.model_worker.feedModel(checked))
        
        # Connect outputs
        self.model_worker.frame_out.connect(self.handle_output)
        self.model_worker.time_out.connect(self.handle_timings)
        self.model_worker.volume_out.connect(self.update_volume)

        self.model_worker.mask_record_out.connect(self.mask_saver.updateCache)
        if self.captureCamera:
            self.captureCamera.mask_sync_trigger.connect(self.mask_saver.writeFromCache)
            
        self.update_model_crop()
        
        self.model_thread.started.connect(self.model_worker.run) 
        self.model_thread.start()
        self.run_model_btn.setChecked(True)

    @Slot(tuple)
    def handle_output(self, data):
        self.latest_boxes = data[0]
        self.latest_masks = data[1]
        self.latest_scores = data[2]

    @Slot(tuple)
    def handle_filter_timings(self, timings):
        process_ms, dropped = timings
        self.filters_total_delay_ms_spbx.setValue(process_ms)
        self.filters_total_delay_frames_spbx.setValue(dropped)

    @Slot(float, float, float)
    def update_volume(self, volume_pl, vol_rate, volume_px3):
        self.volume_spbx.setValue(volume_pl)
        self.latest_volume_pl = volume_pl
        self.latest_vol_rate = vol_rate
        self.latest_volume_px3 = volume_px3

    @Slot(tuple)
    def handle_timings(self, timings):
        inference_time, preprocess_time, frame_delay = timings
        
        self.inference_spbx.setValue(inference_time)
        self.pre_processing_spbx.setValue(preprocess_time)
        self.total_delay_ms_spbx.setValue(inference_time + preprocess_time)
        self.total_delay_frames_spbx.setValue(frame_delay)

    @Slot(object)
    def route_frame_to_model(self, frame):
        if self.model_thread and self.model_thread.isRunning():
            # if len(frame.shape) == 2:
            #     frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

            # if not self.is_key_C_pressed and self.final_crop is not None:
            #     x1, y1, x2, y2 = self.final_crop
            #     frame = frame[y1:y2, x1:x2].copy()
                
            self.model_worker.receiveFrame(frame)

    def update_model_crop(self):
        if getattr(self, 'model_worker', None):
            if not self.is_key_C_pressed and getattr(self, 'final_crop', None):
                x1, y1, x2, y2 = self.final_crop
                self.model_worker.updateCrop((x1, y1, x2 - x1, y2 - y1)) # cx, cy, w, h
            else:
                self.model_worker.updateCrop(None)

    def load_model_file(self):
        model_path, _ = QFileDialog.getOpenFileName(None, "Load Model File", "", "Model Files (*.pt *.onnx, *.engine);;All Files (*)")
        if model_path:
            print(f"Loaded model: {model_path}")
            if self.model_combobox.findText(model_path) == -1:
                self.model_combobox.addItem(model_path) 
            self.model_combobox.setCurrentText(model_path)

    def _init_pump_controls(self):
        self.pump_labels = [self.push1_pressure_label, self.push2_pressure_label]
        self.pump_zero_btns = [self.push1_zero_button, self.push2_zero_button]
        self.pump_apply_btns = [self.push1_apply_button, self.push2_apply_button]
        self.pump_layouts = [self.push1_layout, self.push2_layout]
        self.pump_boxes = [self.push1_setpoint_box, self.push2_setpoint_box]

        for i in range(2):
            self.pump_zero_btns[i].clicked.connect(lambda _, idx=i: self.zero_pressure(idx))
            self.pump_apply_btns[i].clicked.connect(lambda _, idx=i: self.apply_pressure(idx))

    def _init_scrollbar_inputs(self):
        self.scroll_inputs = {
            "push1_setpoint": (self.push1_setpoint_scroll, self.push1_setpoint_box),
            "push2_setpoint": (self.push2_setpoint_scroll, self.push2_setpoint_box),
            "exposure": (self.exposure_scroll, self.exposure_box),
            "gain": (self.gain_scroll, self.gain_box),
            "width": (self.width_scroll, self.width_box),
            "height": (self.height_scroll, self.height_box),
            "target_fps": (self.target_fps_scroll, self.target_fps_box)
        }
        for (scrollbar, spinbox) in self.scroll_inputs.values():
            scrollbar.valueChanged.connect(spinbox.setValue)
            spinbox.valueChanged.connect(scrollbar.setValue)

        self.status_indicators = [self.push1_status, self.push2_status, self.camera_status, self.arduino_status]
        for indicator in self.status_indicators:
            indicator.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            indicator.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def _init_menubar(self):
        # menubar buttons
        self.menubar.setNativeMenuBar(False)
        self.corner = QWidget(self.menubar)
        layout = QHBoxLayout(self.corner)
        layout.setContentsMargins(0, 0, 5, 0)
        self.refreshDevices = QPushButton("Refresh Devices")
        self.calibratePumps = QPushButton("Calibrate Pumps")
        self.reloadWidgets = QPushButton("Reload Widgets")
        dock_widgets = [self.camera_dockwidget, self.camera_controls_dockwidget, self.stage_dockwidget, self.pump_dockwidget, self.yolo_controls_dockwidget]
        layout.addWidget(self.calibratePumps)
        layout.addWidget(self.refreshDevices)
        layout.addWidget(self.reloadWidgets)
        self.menubar.setCornerWidget(self.corner)
        self.refreshDevices.clicked.connect(lambda: self.detect_instruments(force_refresh=True))
        self.calibratePumps.clicked.connect(self.calibrate_pumps)
        self.reloadWidgets.clicked.connect(lambda: [d.show() for d in dock_widgets])

        # menubar actions
        self.actionSave_Config = QAction("Save Config", self)
        self.menuFile.addAction(self.actionSave_Config)
        self.actionSave_Config.triggered.connect(self.save_config)

        self.actionSave_Directory.triggered.connect(self.select_save_directory)
        self.actionLoad_Scripts.triggered.connect(self.load_script_file)

        self.actionLoad_Config = QAction("Load Config", self)
        self.menuFile.addAction(self.actionLoad_Config)
        self.actionLoad_Config.triggered.connect(self.load_config)

        self.actionLoad_Model = QAction("Load Model", self)
        self.menuFile.addAction(self.actionLoad_Model)
        self.actionLoad_Model.triggered.connect(self.load_model_file)

        config_path = Path("config.json")
        self.load_config(config_path)

    def _init_stage_limits(self):
        for spbx in [
            self.x_moveto_currentval_spbx, self.y_moveto_currentval_spbx, self.z_moveto_currentval_spbx,
            self.x_moveto_setpoint_spbx, self.y_moveto_setpoint_spbx, self.z_moveto_setpoint_spbx,
            self.x_moveto_newval_spbx, self.y_moveto_newval_spbx, self.z_moveto_newval_spbx,
            self.x_move_val_spbx, self.y_move_val_spbx, self.z_move_val_spbx
        ]:
            if spbx is not None: # define spinbox limits (xyz)
                spbx.setMinimum(-self.max_distance)
                spbx.setMaximum(self.max_distance)

        for spbx in [
            self.x_speed_currentval_spbx, self.y_speed_currentval_spbx, self.z_speed_currentval_spbx,
            self.x_speed_setpoint_spbx, self.y_speed_setpoint_spbx, self.z_speed_setpoint_spbx,
            self.x_speed_newval_spbx, self.y_speed_newval_spbx, self.z_speed_newval_spbx,
            self.x_accel_currentval_spbx, self.y_accel_currentval_spbx, self.z_accel_currentval_spbx,
            self.x_accel_setpoint_spbx, self.y_accel_setpoint_spbx, self.z_accel_setpoint_spbx,
            self.x_accel_newval_spbx, self.y_accel_newval_spbx, self.z_accel_newval_spbx,
            
            self.x_stepsize_currentval_spbx, self.y_stepsize_currentval_spbx, self.z_stepsize_currentval_spbx,
            self.x_stepsize_newval_spbx, self.y_stepsize_newval_spbx, self.z_stepsize_newval_spbx
        ]:
            if spbx is not None: # define spinbox limits (speed/accel/step)
                spbx.setMinimum(1.0)
                spbx.setMaximum(self.max_speed)

    def _init_stage_controls(self):
        self.arduino_controller = ArduinoController()
        self.arduino_controller.position_updated.connect(self._update_stage_position) # type: ignore
        self.arduino_controller.limits_updated.connect(self._update_stage_limits) # type: ignore
        self.arduino_controller.connection_status_changed.connect(self._update_arduino_connection_status) # type: ignore

        self.x_stage, self.y_stage, self.z_stage = 0, 0, 0
        self.x_actual, self.y_actual, self.z_actual = 0, 0, 0
        self.x_spd, self.y_spd, self.z_spd = 0, 0, 0
        self.x_acc, self.y_acc, self.z_acc = 0, 0, 0
        self.max_distance, self.max_speed, self.max_stepsize = 500000.0, 10000.0, 1000
        
        self.l, self.w, self.h = 500000, 500000, 500000 
        self.x_step, self.y_step, self.z_step = 100, 100, 100

        self.is_key_W_pressed, self.is_key_A_pressed, self.is_key_S_pressed, self.is_key_D_pressed = False, False, False, False
        self.is_key_SHIFT_pressed, self.is_key_SPACE_pressed = False, False

        self.save_label.setText(fr"{self.save_path}/recording_.*")

        self.x_moveto_btn.clicked.connect(lambda _: self._stage_move_abs('x', self.x_moveto_newval_spbx.value())) # type: ignore
        self.y_moveto_btn.clicked.connect(lambda _: self._stage_move_abs('y', self.y_moveto_newval_spbx.value())) # type: ignore
        self.z_moveto_btn.clicked.connect(lambda _: self._stage_move_abs('z', self.z_moveto_newval_spbx.value())) # type: ignore

        self.x_move_btn.clicked.connect(lambda _: self._stage_move_rel('x', self.x_move_val_spbx.value())) # type: ignore
        self.y_move_btn.clicked.connect(lambda _: self._stage_move_rel('y', self.y_move_val_spbx.value())) # type: ignore
        self.z_move_btn.clicked.connect(lambda _: self._stage_move_rel('z', self.z_move_val_spbx.value())) # type: ignore

        self.x_speed_apply_btn.clicked.connect(lambda _: self._stage_apply_kinematics('x', speed=self.x_speed_newval_spbx.value())) # type: ignore
        self.x_accel_apply_btn.clicked.connect(lambda _: self._stage_apply_kinematics('x', accel=self.x_accel_newval_spbx.value())) # type: ignore
        self.x_stepsize_apply_btn.clicked.connect(lambda _: self._stage_apply_stepsize('x', stepsize=self.x_stepsize_newval_spbx.value())) # type: ignore
        
        self.y_speed_apply_btn.clicked.connect(lambda _: self._stage_apply_kinematics('y', speed=self.y_speed_newval_spbx.value()))
        self.y_accel_apply_btn.clicked.connect(lambda _: self._stage_apply_kinematics('y', accel=self.y_accel_newval_spbx.value()))
        self.y_stepsize_apply_btn.clicked.connect(lambda _: self._stage_apply_stepsize('y', stepsize=self.y_stepsize_newval_spbx.value()))
        
        self.z_speed_apply_btn.clicked.connect(lambda _: self._stage_apply_kinematics('z', speed=self.z_speed_newval_spbx.value()))
        self.z_accel_apply_btn.clicked.connect(lambda _: self._stage_apply_kinematics('z', accel=self.z_accel_newval_spbx.value()))
        self.z_stepsize_apply_btn.clicked.connect(lambda _: self._stage_apply_stepsize('z', stepsize=self.z_stepsize_newval_spbx.value()))

        self.set_zero_btn.clicked.connect(self.zero_stage_position)
        self.stop_btn.clicked.connect(self.emergency_stop)

    def _stage_apply_stepsize(self, axis, stepsize):
        if axis == 'x': self.x_step = max(0, min(self.max_stepsize, stepsize))
        if axis == 'y': self.y_step = max(0, min(self.max_stepsize, stepsize))
        if axis == 'z': self.z_step = max(0, min(self.max_stepsize, stepsize))
        self._update_stage_display()

    def _stage_move_abs(self, axis, val): # move stage to absolute coordinate (X, Y, Z)
        if axis == 'x': self.x_stage = max(-self.l, min(self.l, val))
        if axis == 'y': self.y_stage = max(-self.w, min(self.w, val))
        if axis == 'z': self.z_stage = max(-self.h, min(self.h, val))
        self.send_serial(f'C:{int(self.x_stage)}:{int(self.y_stage)}:{int(self.z_stage)}\n')
        self._update_stage_display()

    def _stage_move_rel(self, axis, delta): # move stage by relative distance
        if axis == 'x': self.x_stage = max(-self.l, min(self.l, self.x_stage + delta))
        if axis == 'y': self.y_stage = max(-self.w, min(self.w, self.y_stage + delta))
        if axis == 'z': self.z_stage = max(-self.h, min(self.h, self.z_stage + delta))
        self.send_serial(f'C:{int(self.x_stage)}:{int(self.y_stage)}:{int(self.z_stage)}\n')
        self._update_stage_display()

    def _stage_apply_kinematics(self, axis, speed=-1.0, accel=-1.0): # update real-time stage speed/acceleration, as well as new defaults
        setpoint = getattr(self, f"{axis}_stage")
        if int(speed) == -1:
            speed = getattr(self, f"{axis}_speed_setpoint_spbx").value()
            if speed == 0: speed = 1000
        else:
            getattr(self, f"{axis}_speed_setpoint_spbx").setValue(speed)
            
        if int(accel) == -1:
            accel = getattr(self, f"{axis}_accel_setpoint_spbx").value()
            if accel == 0: accel = 500
        else:
            getattr(self, f"{axis}_accel_setpoint_spbx").setValue(accel)
            
        self.send_serial(f'A:{axis.upper()}:{int(setpoint)}:{int(speed)}:{int(accel)}\n')
        self.send_serial(f'D:SPEED:{int(speed)}\n')
        self.send_serial(f'D:ACCEL:{int(accel)}\n')

    def load_blank(self):
        self.blank = QPixmap("assets/dog.jpg").scaled(self.camera_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.camera_label.setPixmap(self.blank)
        self.camera_label.setAlignment(Qt.AlignCenter)

    def load_config(self, config_path=None): # load presaved window configuration
        if not config_path:
            config_path, _ = QFileDialog.getOpenFileName(None, "Load Config File", "", "json (*.json)")
        if Path(config_path).exists():
            with open(config_path, "r") as f:
                config = json.load(f)
                if "geometry" in config:
                    self.restoreGeometry(QByteArray.fromBase64(config["geometry"].encode('utf-8')))
                if "windowState" in config:
                    self.restoreState(QByteArray.fromBase64(config["windowState"].encode('utf-8')))
                print("Window configuration loaded from config.json.")

    def save_config(self): # save window configuration
        config = {
            "version": 2,
            "geometry": self.saveGeometry().toBase64().data().decode('utf-8'),
            "windowState": self.saveState().toBase64().data().decode('utf-8'),
            "camera": {
                "exposure": self.exposure_box.value() if hasattr(self, 'exposure_box') else 0,
                "gain": self.gain_box.value() if hasattr(self, 'gain_box') else 0,
                "width": self.width_box.value() if hasattr(self, 'width_box') else 1920,
                "height": self.height_box.value() if hasattr(self, 'height_box') else 1200,
                "dynamic_range": self.dynamic_range_cbbx.currentIndex() if hasattr(self, 'dynamic_range_cbbx') else 0,
            },
            "model": {
                "path": self.model_combobox.currentText() if hasattr(self, 'model_combobox') else "",
                "confidence": self.confidence_scrollbar.value() if hasattr(self, 'confidence_scrollbar') else 0.5,
                "ema_enabled": self.ema_chckbx.isChecked() if hasattr(self, 'ema_chckbx') else False,
                "fit_ellipse": self.fit_ellipse_chbx.isChecked() if hasattr(self, 'fit_ellipse_chbx') else False,
            },
            "pumps": {
                "p1_setpoint": self.push1_setpoint_box.value() if hasattr(self, 'push1_setpoint_box') else 0,
                "p2_setpoint": self.push2_setpoint_box.value() if hasattr(self, 'push2_setpoint_box') else 0,
            },
            "stage": {
                "x_step": self.x_step if hasattr(self, 'x_step') else 100,
                "y_step": self.y_step if hasattr(self, 'y_step') else 100,
                "z_step": self.z_step if hasattr(self, 'z_step') else 100,
            },
            "clahe": {
                "enabled": self.clahe_checkbox.isChecked() if hasattr(self, 'clahe_checkbox') else False,
                "clip_limit": self.clip_limit_spbx.value() if hasattr(self, 'clip_limit_spbx') else 2.0,
                "tile_grid": self.tile_grid_spbx.value() if hasattr(self, 'tile_grid_spbx') else 8,
            },
        }
        # Atomic write: write to temp file then rename
        temp_path = "config.json.tmp"
        final_path = "config.json"
        with open(temp_path, "w") as f:
            json.dump(config, f, indent=2)
        import os
        os.replace(temp_path, final_path)
        print("Configuration saved to config.json (v2).")

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return

        key = event.key()
        if key == Qt.Key_Q:
            self.emergency_stop()
            return
        elif key == Qt.Key_O: 
            self.show_overlay = not self.show_overlay
            return
        elif key == Qt.Key_C: 
            self.is_key_C_pressed = True
            return

        is_label_focused = self.camera_label.hasFocus()
        
        # check if thread is actually running)
        if self.videoLoader and self.videoLoader.isRunning() and is_label_focused:
            if key == Qt.Key_Space:
                self.video_paused = not self.video_paused
                self.videoLoader.videoState(self.video_paused)
            elif key == Qt.Key_R:
                self.videoLoader.restartVideo()
            elif key == Qt.Key_X:
                self.videoLoader.clearVideo()
                self.camera_label.clear()
                self.load_blank()
            return

        # camera logic
        if self.captureCamera and self.captureCamera.isRunning() and is_label_focused:
            if self.arduino_controller.is_connected: 
                if key == Qt.Key_W: self.is_key_W_pressed = True
                elif key == Qt.Key_S: self.is_key_S_pressed = True
                elif key == Qt.Key_A: self.is_key_A_pressed = True
                elif key == Qt.Key_D: self.is_key_D_pressed = True
                elif key == Qt.Key_Space: self.is_key_SPACE_pressed = True
                elif key == Qt.Key_Shift: self.is_key_SHIFT_pressed = True

                if any([self.is_key_W_pressed, self.is_key_A_pressed, self.is_key_S_pressed, 
                    self.is_key_D_pressed, self.is_key_SPACE_pressed, self.is_key_SHIFT_pressed]):
                    if not self.stage_move_timer.isActive():
                        self.stage_move_timer.start()
            return

        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return
            
        key = event.key()
        if key == Qt.Key_W: self.is_key_W_pressed = False
        elif key == Qt.Key_S: self.is_key_S_pressed = False
        elif key == Qt.Key_A: self.is_key_A_pressed = False
        elif key == Qt.Key_D: self.is_key_D_pressed = False
        elif key == Qt.Key_Space: self.is_key_SPACE_pressed = False
        elif key == Qt.Key_Shift: self.is_key_SHIFT_pressed = False
        elif key == Qt.Key_C: self.is_key_C_pressed = False

        if not any([self.is_key_W_pressed, self.is_key_A_pressed, self.is_key_S_pressed, 
                    self.is_key_D_pressed, self.is_key_SPACE_pressed, self.is_key_SHIFT_pressed]):
            if self.stage_move_timer.isActive():
                self.stage_move_timer.stop()
        
        super().keyReleaseEvent(event)

    @Slot()
    def _handle_continuous_stage_move(self): 
        # continuously update XYZ target position as long as key booleans remain true, 
        # at self.stage_move_timer frequency (30 Hz)
        moved = False
        if self.is_key_W_pressed:
            self.y_stage += self.y_step
            moved = True
        if self.is_key_S_pressed:
            self.y_stage -= self.y_step
            moved = True
        if self.is_key_A_pressed:
            self.x_stage -= self.x_step
            moved = True
        if self.is_key_D_pressed:
            self.x_stage += self.x_step
            moved = True
        if self.is_key_SPACE_pressed:
            self.z_stage += self.z_step
            moved = True
        if self.is_key_SHIFT_pressed:
            self.z_stage -= self.z_step
            moved = True

        if moved:
            self.x_stage = max(-self.l, min(self.l, self.x_stage))
            self.y_stage = max(-self.w, min(self.w, self.y_stage))
            self.z_stage = max(-self.h, min(self.h, self.z_stage))
            
            self.send_serial(f'C:{int(self.x_stage)}:{int(self.y_stage)}:{int(self.z_stage)}\n')
            self._update_stage_display()

    @Slot(tuple)
    def dispatch_video_frames(self, data):
        """Receives (frame, fps, timestamp, record) from videoLoader.display_out."""
        frame, fps, timestamp, record = data
        current_time = perf_counter()
        if current_time - self.last_frame_time_disp >= 1/30:
            self.update_frame((frame.copy(), fps, 0, timestamp, record))
            self.last_frame_time_disp = current_time
        self.route_frame_to_model(frame)

    def open_video(self):
        file, _ = QFileDialog.getOpenFileName(
            None,
            "Open File",
            "",
            "Video Files (*.avi;*.mp4;*.mov;*.mkv;*.wmv;*.flv;*.mpeg;*.mpg)")
        if file:
            if self.videoLoader is not None:
                self.videoLoader.stop()
            if self.captureCamera:
                self.captureCamera.stop()
            if hasattr(self, 'video_converter') and self.video_converter:
                self.video_converter.stop()
                if hasattr(self, 'video_converter_thread'):
                    self.video_converter_thread.quit()
                    self.video_converter_thread.wait()
                    
            self.videoLoader = processVideo()
            
            # Video path: dispatch to display + model directly
            self.videoLoader.display_out.connect(self.dispatch_video_frames)
            self.videoLoader.frame_out.connect(self.route_frame_to_model)

            self.videoLoader.finished.connect(self.clear_camera_feed)
            self.videoLoader.start()
            self.videoLoader.loadVideo(file)

    @Slot()
    def clear_camera_feed(self):
        cam_active = self.captureCamera is not None and self.captureCamera.isRunning()
        vid_active = self.videoLoader is not None and self.videoLoader.isRunning()
        
        if not cam_active:
            self.captureCamera = None
            self.camera_status.setChecked(False)
            self.camera_status.setText("Disconnected")
            enable_layout(self.camera_controls_layout, False)
            enable_layout(self.recording_layout, False)
            if not vid_active:
                self.camera_label.clear()
                self.load_blank()

    @Slot(str, object, str)
    def _on_device_state_changed(self, name, state, message):
        """Handle device state changes from watchdog."""
        state_str = state.value if hasattr(state, 'value') else str(state)
        self.session_logger.log_device_state_change(name, "previous", state_str, message)
        if name == "camera":
            self.camera_status.setText(f"{state_str}: {message}")
            self.camera_status.setChecked(state_str in ("healthy", "recovering"))
        elif name == "model":
            if hasattr(self, 'model_status'):
                self.model_status.setText(f"{state_str}: {message}")
        elif name == "fluigent":
            if hasattr(self, 'pump_status'):
                for i in range(2):
                    if state_str == "failed":
                        self.pump_status.setText("FAILED")
                        self.pump_status.setChecked(False)
        elif name == "arduino":
            if hasattr(self, 'stage_status'):
                self.stage_status.setText(f"{state_str}")
                self.stage_status.setChecked(state_str in ("healthy", "recovering"))

    @Slot(str, str)
    def _on_critical_failure(self, name, message):
        """Handle critical failures - emergency stop and log."""
        self.session_logger.log_error(name, message, severity="CRITICAL")
        self.emergency_stop()
    @Slot(tuple)
    def update_frame(self, data):
        frame, fps, actual_fps, timestamp, recording = data
        self.actual_fps = actual_fps

        self.latest_frame_shape = frame.shape
        if len(frame.shape) == 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        h, w, ch = frame.shape
        bytes_per_line = w * ch

        if self.is_key_C_pressed and self.crop_start and self.crop_end:
            cv2.rectangle(frame, self.crop_start, self.crop_end, (0, 0, 255), 2)
        elif not self.is_key_C_pressed and self.final_crop and self.show_overlay:
            x1, y1, x2, y2 = self.final_crop
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        if self.show_overlay:
            fontScale = 1.5
            thickness = 2

            ms = timestamp * 1e3
            minutes = int(ms // 60000)
            seconds = int((ms % 60000) // 1000)
            hundredths = int((ms % 1000) // 10)
            timestamp_str = f"{minutes:02d}:{seconds:02d}:{hundredths:02d}"
                
            messages = [f"CAMERA FPS: {fps:.2f}", f"ACTUAL FPS: {actual_fps:.2f}", f'TIMESTAMP: {timestamp_str}']

            if actual_fps == 0:
                messages.pop(1)
            
            total_height = 0
            for msg in messages:
                rect, pos = textBackground(msg, fontScale, thickness, (5, total_height))
                cv2.rectangle(frame, rect[0], rect[1], color=(255, 255, 255), thickness=-1)
                cv2.putText(frame, msg, pos, cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0,0,0), thickness, lineType=cv2.LINE_AA)
                total_height += 5+rect[1][1]-rect[0][1]

        if self.model_thread and self.model_thread.isRunning() and self.feedframes_chkbox.isChecked():
            if hasattr(self, 'latest_boxes'):
                
                # get offset from crop if active
                cx, cy, crop_w, crop_h = 0, 0, w, h
                if not self.is_key_C_pressed and self.final_crop:
                    cx, cy = self.final_crop[0], self.final_crop[1]
                    crop_w, crop_h = self.final_crop[2] - cx, self.final_crop[3] - cy

                for box, mask, conf in zip(self.latest_boxes, self.latest_masks, self.latest_scores):
                    bx1, by1, bx2, by2 = map(int, box[:4])
                    if conf == "K":
                        label = "KF"
                        color = (0, 165, 255) # Orange for Kalman predictions
                    else:
                        label = f"{conf:.2f}"
                        color = (0, 255, 0) # Green for real model detections
                    
                    # resize mask to the cropped area dimensions
                    if mask.shape[:2] != (crop_h, crop_w):
                        mask_resized = cv2.resize(mask, (crop_w, crop_h), interpolation=cv2.INTER_NEAREST)
                    else:
                        mask_resized = mask

                    crop_region = frame[cy:cy+crop_h, cx:cx+crop_w]
                    color_overlay = crop_region.copy()
                    color_overlay[mask_resized > 0] = color
                    cv2.addWeighted(color_overlay, 0.4, crop_region, 0.6, 0, dst=crop_region)
                    
                    # draw bounding box using global offsets
                    gx1, gy1, gx2, gy2 = bx1 + cx, by1 + cy, bx2 + cx, by2 + cy
                    cv2.rectangle(frame, (gx1, gy1), (gx2, gy2), color, 2)
                    
                    (rw, rh), b = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                    cv2.rectangle(frame, (gx2 - rw, gy1 - rh - b - 5), (gx2, gy1 - 5), color, -1)
                    cv2.putText(frame, label, (gx2 - rw, gy1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        else:
            self.latest_boxes = []
            self.latest_masks = []
            self.latest_scores= []
            self.pre_processing_spbx.setValue(0)
            self.inference_spbx.setValue(0)
            self.total_delay_ms_spbx.setValue(0)
            self.total_delay_frames_spbx.setValue(0)

        q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(q_image).scaled(self.camera_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.p_shape = (pixmap.width(), pixmap.height()) 
        self.camera_label.setPixmap(pixmap)

    @Slot(int, int)
    def update_record_progress(self, written, total):
        if total > 0:
            pct = (written / total) * 100.0
            # Cap visual at 99.9% until the destructor confirms the file is fully closed
            pct = min(pct, 99.9) 
            self.record_button.setText(f"Writing to file: {pct:.2f}%")

    @Slot()
    def finish_recording(self):
        # Triggered when FFmpeg completely releases the file lock
        self.record_button.setEnabled(True)
        self.record_button.setText("Start Recording")
        self.compress_btn.setEnabled(True)

    def toggle_recording(self):
        if self.is_recording:
            self.is_recording = False
            
            # Immediately lock the UI and set status
            self.record_button.setEnabled(False)
            self.record_button.setText("Finalizing...")
            
            # Remove the red border instantly so the user knows capture has stopped
            self.camera_frame.setStyleSheet("""
                QFrame#camera_frame {
                    border: none;
                    background-color: transparent;
                    outline: none;
                }
            """)
            
            self.release_mask_writer.emit()
            self.captureCamera.stopRecord()
                
            # Perform quick CSV save
            save_file = Path(self.save_path) / f"recording_{int(self.start_time)}.csv"
            df = pd.DataFrame(self.data)
            df.to_csv(save_file, index=False)
            print(f"Data saved to {save_file}")
            
            # Reset datastore
            self.data = {
                "timestamps": [], "p1_measured": [], "p2_measured": [], "p1_setpoint": [], "p2_setpoint": [],
                "x": [], "y": [], "z": [], "x_setpoint": [], "y_setpoint": [], "z_setpoint": [],
                "arduino_time": [], "box_x1": [], "box_y1": [], "box_x2": [], "box_y2": [], "box_conf": [],
                "volume_px3": [], "volume_pl": []
            }

            self.save_label.setText(fr"{self.save_path}/recording_.*")
            self.camera_frame.setStyleSheet("""
                QFrame#camera_frame {
                    border: none;
                    background-color: transparent;
                    outline: none;
                }
            """)
        else:
            self.start_time = time()
            compress = self.compress_btn.isChecked()
            ext = '.mkv'
            self.save_label.setText(fr"{self.save_path}/recording_{int(self.start_time)}.{ext}")

            if self.captureCamera and self.captureCamera.isRunning():
                self.captureCamera.startRecord(f"recording_{int(self.start_time)}", self.save_path, compress)
                
                # Initialize mask writer locally via signal
                mask_filename = f'{self.save_path}/recording_{int(self.start_time)}_mask{ext}'
                w, h = self.captureCamera.frame_size
                camera_fps = self.captureCamera.desired_fps 
                
                # Dispatch creation to background thread (is_16bit=False for masks)
                self.start_mask_record.emit(mask_filename, camera_fps, (w, h), False, compress)
            
            self.is_recording = True
            self.compress_btn.setEnabled(False)
            self.record_button.setText("Stop Recording")
            print(f"Recording started (Compressed: {compress})...")
            self.camera_frame.setStyleSheet("""
                QFrame#camera_frame {
                    border: 3px solid red;
                    border-radius: 5px; 
                    background-color: transparent;
                }
            """)

    def take_screenshot(self):
        if self.captureCamera and self.captureCamera.isRunning():
            # Saves as lossless TIFF natively supporting 8-bit or 16-bit
            filepath = str(Path(self.save_path) / "screenshot")
            self.captureCamera.takeScreenshot(filepath)
        else:
            print("Camera not running. Cannot take screenshot.")

    def calibrate_pumps(self):
        n = self.controller.num_channels if self.controller and self.controller.initialized else 0
        for i in range(n):
            self.controller.calibrate_pump(i)

    def _register_for_usb_notifications(self):
        if sys.platform != 'win32': # incompatible with non-windows systems
            return
        try:
            user32 = ctypes.windll.user32
            RegisterDeviceNotification = user32.RegisterDeviceNotificationW
            RegisterDeviceNotification.restype = ctypes.c_void_p
            RegisterDeviceNotification.argtypes = [wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD]

            dev_broadcast_interface = DEV_BROADCAST_DEVICEINTERFACE_W()
            dev_broadcast_interface.dbcc_size = ctypes.sizeof(DEV_BROADCAST_DEVICEINTERFACE_W)
            dev_broadcast_interface.dbcc_devicetype = DBT_DEVTYP_DEVICEINTERFACE
            dev_broadcast_interface.dbcc_classguid = GUID_DEVINTERFACE_USB_DEVICE

            hwnd = self.winId()

            self.notification_handle = RegisterDeviceNotification(
                hwnd,
                ctypes.byref(dev_broadcast_interface),
                DEVICE_NOTIFY_WINDOW_HANDLE
            )

            if self.notification_handle:
                print("Successfully registered for USB device notifications.")
            else:
                print(f"Failed to register for USB device notifications. Error: {ctypes.get_last_error()}")
        except Exception as e:
            print(f"Error registering for device notifications: {e}")

    def nativeEvent(self, eventType, message):
            # Intercept Windows USB arrival notifications
            if eventType == b"windows_generic_MSG":
                msg = wintypes.MSG.from_address(message.__int__())
                if msg.message == WM_DEVICECHANGE:
                    if msg.wParam == DBT_DEVICEARRIVAL:
                        print("USB Device inserted! Waiting for drivers to mount...")
                        # Delay scanning by 2 seconds so the camera driver finishes loading
                        QTimer.singleShot(2000, lambda: self.detect_instruments(force_refresh=False))
            return super().nativeEvent(eventType, message)

    def detect_instruments(self, force_refresh=False):
        # automatically scans for any connected hardware that hasn't been initialized yet
        if force_refresh:
            print("Forcing refresh of Fluigent controller...")
            if self.controller:
                self.controller.close()
            self.controller = FluigentController()

        print("Detecting Arduino...")
        self.arduino_controller.connect() 

        self.controller.initialize()

        if not self.controller.initialized:
            print("Fluigent controller not initialised (no hardware found?)")
            self.pumps_found = False
            for i in range(2):
                self.status_indicators[i].setText("Disconnected")
                self.status_indicators[i].setChecked(False)
                enable_layout(self.pump_layouts[i], False)
        else:
            num_pumps = self.controller.find_pumps()
            if num_pumps and num_pumps > 0:
                self.pumps_found = True
                n = min(num_pumps, 2)  # Clamp to UI capacity (2 pumps shown)
                for i in range(2):
                    connected = i < n
                    self.status_indicators[i].setChecked(connected)
                    self.status_indicators[i].setText("Connected" if connected else "Disconnected")
                    enable_layout(self.pump_layouts[i], connected)
                for i in range(n):
                    try:
                        p_min, p_max = self.controller.get_range(i)
                        for input in self.scroll_inputs[f"push{i+1}_setpoint"]:
                            input.setRange(p_min, p_max)
                    except Exception as e:
                        print(f"Pump {i} range error: {e}")
                print(f"Detected {num_pumps} pump channel(s), using {n} in UI.")
            else:
                self.pumps_found = False
                for i in range(2):
                    self.status_indicators[i].setChecked(False)
                    self.status_indicators[i].setText("Disconnected")
                    enable_layout(self.pump_layouts[i], False)
                print("No pump channels found!")

        camera_is_running = self.captureCamera and self.captureCamera.isRunning()

        if force_refresh and camera_is_running:
            print("Forcing refresh of camera...")
            self.captureCamera.stop()
            self.captureCamera = None
            camera_is_running = False

        if not camera_is_running:
            self.tlf = py.TlFactory.GetInstance()
            cameras = self.tlf.EnumerateDevices()
            _f = False
            for c in cameras:
                name = c.GetModelName()
                if name == "a2A1920-160umBAS":
                    try:
                        print("a2A1920-160umBAS found!")
                        _f = True
                        self.open_camera(c)
                        break
                    except Exception as e:
                        print(f"Error finding to a2A1920-160umBAS: {e}")
            if not _f:
                print("a2A1920-160umBAS not found!")
                self.camera_status.setChecked(False)
                self.camera_status.setText("Disconnected")
                if self.captureCamera:
                    self.captureCamera.stop()
                    self.captureCamera = None
        else:
            print("Camera already running, skipping camera detection.")

    def open_camera(self, c):
        if self.videoLoader:
            self.videoLoader.stop()
        if not c.__class__.__name__ == "DeviceInfo":
            print(f"Invalid camera object: {c.__class__.__name__}")
            return
        
        self.captureCamera = captureCamera(c, self.target_fps_box.value(), c.GetModelName(), self.tlf)
        self.captureCamera.watchdog = self.watchdog
        self.watchdog.register_device("camera", expected_hz=100,
                                      reconnect_callback=lambda: self.open_camera(c))
        self.captureCamera.display_out.connect(self.update_frame)
        self.captureCamera.finished.connect(self.clear_camera_feed)
        self.captureCamera.frame_out_for_model.connect(self.route_frame_to_model)
        self.captureCamera.timestamp.connect(self.record_data_row)
        print("Connected to a2A1920-160umBAS!")
        self.captureCamera.start()
        self.captureCamera.startCamera()

        # Connect the new UI tracking signals
        self.captureCamera.record_progress.connect(self.update_record_progress)
        self.captureCamera.record_finished.connect(self.finish_recording)

        limits = self.captureCamera.limits
        vals = self.captureCamera.current_vals

        if getattr(self, '_camera_ui_connected', False):
            for signal in [self.exposure_box.valueChanged, 
                           self.gain_box.valueChanged, 
                           self.width_box.valueChanged, 
                           self.height_box.valueChanged, 
                           self.dynamic_range_cbbx.currentIndexChanged]:
                # Disconnects safely; passing 0 suppresses the C++ warning if no slots exist
                try:
                    signal.disconnect(0) 
                except (RuntimeError, TypeError):
                    pass
    

        if limits:
            for name, spinbox, scroll in [
                ("exposure", self.exposure_box, self.exposure_scroll),
                ("gain", self.gain_box, self.gain_scroll),
                ("width", self.width_box, self.width_scroll),
                ("height", self.height_box, self.height_scroll)
            ]:
                spinbox.setRange(int(limits[name][0]), int(limits[name][1]))
                scroll.setRange(int(limits[name][0]), int(limits[name][1]))
            
            
            self.exposure_box.valueChanged.connect(self.captureCamera.setExposure)
            self.gain_box.valueChanged.connect(self.captureCamera.setGain)
            self.width_box.valueChanged.connect(self.captureCamera.setWidth)
            self.height_box.valueChanged.connect(self.captureCamera.setHeight)
            self.dynamic_range_cbbx.currentIndexChanged.connect(self.captureCamera.setDynamicRange)

            self.width_box.setValue(int(limits["width"][1]))
            self.height_box.setValue(int(limits["height"][1]))

            # Force the hardware to adopt whatever parameters your UI currently displays
            self.captureCamera.setExposure(self.exposure_box.value())
            self.captureCamera.setGain(self.gain_box.value())
            self.captureCamera.setWidth(self.width_box.value())
            self.captureCamera.setHeight(self.height_box.value())
            self.captureCamera.setDynamicRange(self.dynamic_range_cbbx.currentIndex())

        enable_layout(self.camera_controls_layout, True)
        enable_layout(self.recording_layout, True)
        self.camera_status.setText("Connected")
        self.camera_status.setChecked(True)
        self._camera_ui_connected = True

    def apply_pressure(self, pump_idx):
        pressure = self.scroll_inputs[f"push{pump_idx+1}_setpoint"][0].value()
        self.controller.set_pressure(pump_idx, pressure)

    def zero_pressure(self, pump_idx):
        self.controller.zero_pump(pump_idx)
        self.pump_boxes[pump_idx].setValue(0.0)

    def send_serial(self, command: str):
        self.arduino_controller.send_command(command)

    def zero_stage_position(self):
        self.send_serial("Z\n")
        # Sync local Python variables so it doesn't snap back to old coordinates on next move
        self.x_stage = self.y_stage = self.z_stage = 0
        self._update_stage_display()

    def emergency_stop(self):
        print("STOP TRIGGERED: Halting stage and zeroing pressures.")
        self.session_logger.log_event("emergency_stop", {})
        # Stop stage movement instantly
        self.send_serial("S\n") 
        self.x_stage, self.y_stage, self.z_stage = self.x_actual, self.y_actual, self.z_actual
        self._update_stage_display()
        
        # Stop pumps and reset UI
        if self.controller and self.controller.initialized:
            for i in range(self.controller.num_channels):
                self.zero_pressure(i)
                
        # Halt any running scripts
        if self.script_runner.isRunning():
            self.script_runner.stop_script()

        # Stop model feed
        if hasattr(self, 'model_thread') and self.model_thread:
            self.model_thread.feed = False
            self.feedframes_chkbox.setChecked(False)

    @Slot(bool, str)
    def _update_arduino_connection_status(self, connected: bool, message: str):
        if connected:
            self.arduino_status.setText("Connected")
            self.arduino_status.setChecked(True)
            enable_layout(self.stage_layout, True)
            print(message)
        else:
            self.arduino_status.setText("Disconnected")
            self.arduino_status.setChecked(False)
            enable_layout(self.stage_layout, False)
            print(message)
            self.x_actual = self.y_actual = self.z_actual = 0
            self.x_stage = self.y_stage = self.z_stage = 0
            self._update_stage_display()

    @Slot(int, int, int, int, int, int, float, float, float, float, float, float)
    def _update_stage_position(self, x: int, y: int, z: int, xs: int, ys: int, zs: int, 
                               xspd: float, yspd: float, zspd: float, 
                               xacc: float, yacc: float, zacc: float):
        #print(x, y, z, xs, ys, zs, xspd, yspd, zspd, xacc, yacc, zacc)
        self.x_actual = x
        self.y_actual = y
        self.z_actual = z
        
        # Sync the internal GUI state perfectly with the hardware's internal setpoints
        self.x_stage = xs
        self.y_stage = ys
        self.z_stage = zs
        
        # Sync current speeds and accelerations
        self.x_spd = np.abs(xspd)
        self.y_spd = np.abs(yspd)
        self.z_spd = np.abs(zspd)
        self.x_acc = np.abs(xacc)
        self.y_acc = np.abs(yacc)
        self.z_acc = np.abs(zacc)

        self._update_stage_display()

    @Slot(int, int, int)
    def _update_stage_limits(self, l: int, w: int, h: int):
        self.l = l
        self.w = w
        self.h = h
        
        # Adjust internal software limits dynamically 
        for ax, lim in [('x', self.l), ('y', self.w), ('z', self.h)]:
            obj1 = getattr(self, f'{ax}_moveto_newval_spbx', None)
            if obj1: obj1.setRange(-lim, lim)

            obj2 = getattr(self, f'{ax}_move_val_spbx', None)
            if obj2: obj2.setRange(-lim*2, lim*2)

        self._update_stage_display() 

    def _update_stage_display(self):
        # updates UI elements robustly while explicitly blocking signals to prevent looping
        
        def safe_set(spbx, val):
            if spbx:
                try:
                    # Dynamically check if the spinbox expects an int or a float
                    val_type = type(spbx.value())
                    casted_val = val_type(val)
                    
                    if spbx.value() != casted_val:
                        spbx.blockSignals(True)
                        spbx.setValue(casted_val)
                        spbx.blockSignals(False)
                except Exception as e:
                    print(f"Error setting spinbox: {e}")

        # Actual Positions
        safe_set(self.x_moveto_currentval_spbx, self.x_actual)
        safe_set(self.y_moveto_currentval_spbx, self.y_actual)
        safe_set(self.z_moveto_currentval_spbx, self.z_actual)

        # Software Setpoints
        safe_set(self.x_moveto_setpoint_spbx, self.x_stage)
        safe_set(self.y_moveto_setpoint_spbx, self.y_stage)
        safe_set(self.z_moveto_setpoint_spbx, self.z_stage)
        
        # Current Speeds
        safe_set(self.x_speed_currentval_spbx, self.x_spd)
        safe_set(self.y_speed_currentval_spbx, self.y_spd)
        safe_set(self.z_speed_currentval_spbx, self.z_spd)

        # Configured Accelerations
        safe_set(self.x_accel_currentval_spbx, self.x_acc)
        safe_set(self.y_accel_currentval_spbx, self.y_acc)
        safe_set(self.z_accel_currentval_spbx, self.z_acc)

        # Current Step Sizes
        safe_set(self.x_stepsize_currentval_spbx, self.x_step)
        safe_set(self.y_stepsize_currentval_spbx, self.y_step)
        safe_set(self.z_stepsize_currentval_spbx, self.z_step)

    def update_pump_info(self):
        if not self.pumps_found:
            for i in range(2):
                self.status_indicators[i].setText("Disconnected")
                self.pump_labels[i].setText("-1")
                self.status_indicators[i].setChecked(False)
                enable_layout(self.pump_layouts[i], False)
            return

        num_pumps = min(self.controller.num_channels, 2)
        for i in range(2):
            if i >= num_pumps:
                self.status_indicators[i].setText("Disconnected")
                self.pump_labels[i].setText("-1")
                self.status_indicators[i].setChecked(False)
                enable_layout(self.pump_layouts[i], False)
                continue

            pressure = self.controller.get_pressure(i)
            if self.controller.calibrating[i]:
                self.status_indicators[i].setText("Calibrating")
                enable_layout(self.pump_layouts[i], False)
            else:
                is_connected = pressure != -1
                self.status_indicators[i].setText("Connected" if is_connected else "Disconnected")
                self.pump_labels[i].setText(f'{pressure:.4f}' if is_connected else "-1")
                self.status_indicators[i].setChecked(is_connected)
                enable_layout(self.pump_layouts[i], is_connected)

        self.current_pressures = [
            self.controller.get_pressure(i) if i < num_pumps and self.controller.get_pressure(i) != -1 else 0.0
            for i in range(2)
        ]

    @Slot(float)
    def record_data_row(self, timestamp):
        if not self.is_recording: return
        
        # 1. Append Hardware Data
        self.data["timestamps"].append(timestamp)
        self.data["p1_measured"].append(self.current_pressures[0])
        self.data["p2_measured"].append(self.current_pressures[1])
        self.data["p1_setpoint"].append(self.controller.setpoint_pressures[0])
        self.data["p2_setpoint"].append(self.controller.setpoint_pressures[1])

        ac = self.arduino_controller
        self.data["x"].append(ac.latest_x if hasattr(ac, 'latest_x') else 0)
        self.data["y"].append(ac.latest_y if hasattr(ac, 'latest_y') else 0)
        self.data["z"].append(ac.latest_z if hasattr(ac, 'latest_z') else 0)
        self.data["x_setpoint"].append(ac.latest_xs if hasattr(ac, 'latest_xs') else 0)
        self.data["y_setpoint"].append(ac.latest_ys if hasattr(ac, 'latest_ys') else 0)
        self.data["z_setpoint"].append(ac.latest_zs if hasattr(ac, 'latest_zs') else 0)
        self.data["arduino_time"].append(ac.latest_arduino_time if hasattr(ac, 'latest_arduino_time') else 0)
        self.data["volume_pl"].append(getattr(self, 'latest_volume_pl', 0.0))
        self.data["volume_px3"].append(getattr(self, 'latest_volume_px3', 0.0))

        # 2. Append Model Data (Accounting for Crop offsets)
        cx, cy = 0, 0
        if not self.is_key_C_pressed and getattr(self, 'final_crop', None):
            cx, cy = self.final_crop[0], self.final_crop[1]
            
        if hasattr(self, 'latest_boxes') and len(self.latest_boxes) > 0:
            box = self.latest_boxes[0]
            self.data["box_x1"].append(box[0] + cx)
            self.data["box_y1"].append(box[1] + cy)
            self.data["box_x2"].append(box[2] + cx)
            self.data["box_y2"].append(box[3] + cy)
            self.data["box_conf"].append(self.latest_scores[0])
        else:
            self.data["box_x1"].append(0)
            self.data["box_y1"].append(0)
            self.data["box_x2"].append(0)
            self.data["box_y2"].append(0)
            self.data["box_conf"].append(0)

    def select_save_directory(self):
        save_path = QFileDialog.getExistingDirectory(None, "Select Save Directory", "")
        if save_path:
            self.save_path = save_path
            self.save_label.setText(fr"{self.save_path}/recording_*.")

    def run_script(self):
        script_path = self.script_combobox.currentText()
        if script_path:
            print(f"Running script: {script_path}")
            with open(script_path, 'r') as f:
                script = json.load(f)
                self.send_script_signal.emit(script)
        else:
            print("No script selected!")

    def load_script_file(self):
        script_path, _ = QFileDialog.getOpenFileName(None, "Load Script File", "", "json (*.json)")
        if script_path:
            print(f"Loaded script: {script_path}")
            self.script_combobox.addItem(script_path) 
            self.script_combobox.setCurrentText(script_path) 

    def closeEvent(self, event: QCloseEvent) -> None: 
        try:
            if self.data["timestamps"] and self.save_path:
                save_file = Path(self.save_path) / f"recording_{int(self.start_time)}.csv"
                df = pd.DataFrame(self.data)
                df.to_csv(save_file, index=False)
                print(f"Data saved to {save_file}")

            if self.is_recording:
                print("Stopping active recording before exit...")
                self.toggle_recording()
                
            self.controller.close()

            threads_to_stop = [
                self.script_runner, 
                self.videoLoader, 
                self.captureCamera
            ]
            for thread in threads_to_stop:
                if thread:
                    print(f"Stopping thread: {thread.__class__.__name__}")
                    thread.stop()

            if hasattr(self, 'mask_saver_thread') and self.mask_saver_thread.isRunning():
                self.release_mask_writer.emit() # Safely ensure lock is destroyed
                sleep(0.1) # tiny sleep to ensure emission propagates
                self.mask_saver_thread.quit()
                self.mask_saver_thread.wait()

            self.stop_model() # Uses your existing clean-up logic

            if hasattr(self, 'videoLoader') and self.videoLoader:
                self.videoLoader.stop()

            if hasattr(self, 'watchdog') and self.watchdog:
                self.watchdog.stop_monitoring()

            self.arduino_controller.close() 
            event.accept()
            pass
        except Exception as e:
            print(f'Error closing program: {e}')
            event.accept()
        print('\nExited')

if not QApplication.instance():
    app = QApplication(sys.argv)
else:
    app = QApplication.instance()

if __name__ == '__main__':
    window = MainWindow()
    app.setStyle('Windows') # type: ignore
    window.show()
    window.load_blank()
    app.exec() # type: ignore