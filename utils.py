# fluigent dependencies
from Fluigent.SDK import fgt_detect, fgt_init, fgt_close # type: ignore
from Fluigent.SDK import fgt_calibratePressure, fgt_get_pressureChannelCount, fgt_get_pressureStatus # type: ignore
from Fluigent.SDK import fgt_set_pressure, fgt_get_pressure, fgt_get_pressureRange # type: ignore

from functools import wraps
import logging
from PySide6.QtCore import QThread, QObject, Slot, QMutexLocker, QMutex, Signal, QTimer, QIODevice
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo 
import cv2

def check_connection(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.check():
            return None
        return method(self, *args, **kwargs)
    return wrapper

class FluigentController():
    def __init__(self):
        self.SN = []
        _ = self.detect()
        self.initialized=False
        self.num_channels = 0
        self.calibrating = []  # Will be sized after init
        self.setpoint_pressures = []  # Will be sized after init

    def detect(self):
        SNs, _ = fgt_detect()
        controllerCount = len(SNs)
        if controllerCount > 0:
            self.SN = SNs
            return True
        else:   
            print("No controllers detected!")
            return False

    def check(self):
        if not self.initialized:
            return False
        for i in range(self.num_channels):
            if self.get_pressure(i) == -1:
                print(f"No pumps connected (channel {i} failed)!")
                return False
        return True

    def initialize(self):
        if not self.SN:
            print("No Fluigent controllers detected to initialize!")
            return
        try:
            fgt_init(self.SN)
            self.initialized = True
            # Determine number of pressure channels dynamically
            self.num_channels = int(fgt_get_pressureChannelCount())
            self.calibrating = [False] * self.num_channels
            self.setpoint_pressures = [0.0] * self.num_channels
            print(f"Fluigent initialized: {self.num_channels} pressure channel(s)")
        except Exception as e:
            print(f"FluigentController: initialisation error: {e}")
            self.initialized = False

    @check_connection
    def find_pumps(self):
        return int(fgt_get_pressureChannelCount())

    @check_connection
    def set_pressure(self, pump_idx, pressure, stdout=True):
        fgt_set_pressure(pump_idx, pressure)
        self.setpoint_pressures[pump_idx] = pressure
        pressureMeasurement = fgt_get_pressure(pump_idx)
        if stdout:
            l1, l2 = f"Setpoint", f"Current pressure:"
            output = (f"[{pump_idx+1:<1}] {l1:<18} {int(pressure)} mBar\n"
                      f"{'':<3} {l2:<18}{pressureMeasurement:.4f} mBar")
            print(output)

    def get_pressure(self, pump_idx) -> float:
        if self.initialized:
            logging.disable(logging.CRITICAL) 
            error, pressure = fgt_get_pressure(pump_idx, get_error = True)
            if error == error.Calibrating:
                self.calibrating[pump_idx] = True
                return 0.0
            elif error == error.USB_error or error == error.No_instr_found:
                print(f'Pump {pump_idx+1} disconnected! Closing instance.')
                self.close()
                return -1
            self.calibrating[pump_idx] = False
            logging.disable(logging.NOTSET)
            return pressure
        return -1

    @check_connection
    def get_range(self, pump_idx) -> tuple:
        minPressure, maxPressure = fgt_get_pressureRange(pump_idx)
        return (minPressure, maxPressure)

    @check_connection
    def reset_all(self):
        if self.initialized:
            n = int(fgt_get_pressureChannelCount())
            for pump_idx in range(n):
                fgt_set_pressure(pump_idx, 0)

    def zero_pump(self, pump_idx):
        self.set_pressure(pump_idx, 0)

    @check_connection
    def calibrate_pump(self, pump_idx):
        print(f'Calibrating pump: {pump_idx+1}')
        fgt_calibratePressure(pump_idx)

    def close(self):
        fgt_close()
        self.initialized = False

def enable_layout(layout, enabled: bool):
    """Recursively sets the enabled state for all widgets in a layout."""
    for i in range(layout.count()):
        item = layout.itemAt(i)
        widget = item.widget()
        
        if widget is not None:
            widget.setEnabled(enabled)
        elif item.layout() is not None:
            enable_layout(item.layout(), enabled)

def textBackground(text, fontScale, thickness, pos):
    (textWidth, textHeight), baseline = cv2.getTextSize(str(text), cv2.FONT_HERSHEY_SIMPLEX, fontScale, thickness)
    rect = [(pos[0], pos[1]), (pos[0] + textWidth, pos[1] + textHeight+baseline)]
    textPos = (pos[0], pos[1] + textHeight + baseline // 2)
    return (rect, textPos)

class scriptRunner(QThread):
    feed_signal = Signal(bool)
    stage_signal = Signal(str, float)
    pump_signal = Signal(int, float)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.controller_mutex = QMutex()
        self.running = False
        self._current_script = None
        self._script_pending = False     

    def run(self):
        while self.running:
            script_to_run = None
            try:
                with QMutexLocker(self.controller_mutex):
                    if self._script_pending:
                        script_to_run = self._current_script
                        self._script_pending = False
                    else:
                        self.running = False
                        break
                if script_to_run:
                    try:
                        for cmd in script_to_run:
                            with QMutexLocker(self.controller_mutex):
                                if not self.running:
                                    break
                            self.execute_command(cmd)
                    except Exception as e:
                        print(f"Error in script thread: {e}")
                    finally:
                        print("Script execution finished.")
                        self.running = False
            except Exception as e:
                print(f"Error running script: {e}")

    @Slot(list)
    def runScript(self, script):
        with QMutexLocker(self.controller_mutex):
            self._current_script = script
            self._script_pending = True
            self.running = True
        if not self.isRunning():
            self.start()

    def execute_command(self, cmd):
        arduino = self.main_window.arduino_controller
        for key, value in cmd.items():
            key_lower = key.lower()

            if key_lower == "set_pressure":
                channel = value["channel"] - 1
                pressure = value["pressure"]
                self.pump_signal.emit(channel, float(pressure))
                print(f"SET PRESSURE: c={channel+1}, p={pressure} mBar")
            
            elif key_lower == "wait":
                print(f"WAIT: {value} ms")
                self.msleep(value)
            
            elif key_lower == "feed":
                print(f"FEED: {value}")
                self.feed_signal.emit(bool(value))
            
            elif key_lower == "loop":
                count = value.get("count", 1)
                commands = value.get("commands", [])
                cmds_str = "\n".join(str(cmd) for cmd in commands)
                print(f"LOOP:\n{cmds_str}\nRepeating {count} times")
                for i in range(count):
                    if not self.running: break
                    print(f"  --- Loop Iteration {i+1}/{count} ---")
                    for sub_cmd in commands:
                        if not self.running: break
                        self.execute_command(sub_cmd) # Recursive call
            
            elif key_lower == "move_wait":
                axis = value.get("axis", "x").lower()
                dist = value.get("distance", 0.0)
                print(f"MOVE_WAIT: Moving {axis} by {dist} and waiting...")
                
                # Emit move command to main thread
                self.stage_signal.emit(f"move_{axis}", float(dist))
                
                # Tiny sleep to ensure the command reaches the Arduino and it starts moving
                self.msleep(150)
                
                # Poll Arduino speed until it drops back to 0
                if arduino:
                    while self.running:
                        spd = getattr(arduino, f"latest_{axis}spd", 0.0)
                        if spd == 0.0:
                            break
                        self.msleep(33)
                else:
                    print("Warning: arduino_controller not linked. Skipping wait.")

            elif any(key_lower.startswith(prefix) for prefix in ["move_", "speed_", "accel_"]):
                print(f"STAGE CMD: {key_lower} = {value}")
                self.stage_signal.emit(key_lower, float(value))

            elif key_lower == "deposit":
                channel = value.get("channel", 1) - 1
                pressure = value.get("pressure", 0.0)
                target_volume = value.get("target_volume", 0.0)
                lookahead_ms = value.get("lookahead_ms", 100.0)
                
                # Pre-deposit validation
                ok, msg = self._validate_deposit_preconditions(channel, pressure, target_volume)
                if not ok:
                    print(f"DEPOSIT ABORTED: {msg}")
                    continue
                
                print(f"DEPOSIT: Ch {channel+1} at {pressure} mBar -> {target_volume} pL (Lookahead: {lookahead_ms}ms)")
                
                self.pump_signal.emit(channel, float(pressure))
                self.feed_signal.emit(True)
                self.feedback_loop(channel, target_volume, lookahead_ms)

            else:
                print(f"Unknown command: {key}")

    def feedback_loop(self, channel, target_volume, lookahead_ms):
        # Event-driven: wait for volume update signal instead of polling
        volume_cond = QWaitCondition()
        volume_mutex = QMutex()
        
        def on_volume(vol_pl, vol_rate, vol_px3):
            volume_cond.wakeAll()
        self.main_window.script_runner.volume_update = on_volume
        
        MAX_REASONABLE_VOL = 5000
        MAX_REASONABLE_RATE = 500
        
        while self.running:
            current_vol = getattr(self.main_window, 'latest_volume_pl', 0.0)
            vol_rate = getattr(self.main_window, 'latest_vol_rate', 0.0)
            
            # Sanity bounds check
            if current_vol > MAX_REASONABLE_VOL or vol_rate > MAX_REASONABLE_RATE:
                self.pump_signal.emit(channel, 0.0)
                self.feed_signal.emit(False)
                print(f"DEPOSIT ABORT: Volume out of bounds (vol={current_vol:.1f}, rate={vol_rate:.1f})")
                break
            
            # Fetch actual FPS (fallback to 30 if disconnected or starting up)
            fps = getattr(self.main_window, 'actual_fps', 30.0)
            if fps <= 0: fps = 30.0 
            
            # Convert lookahead ms to dynamic frames ahead
            frames_ahead = (lookahead_ms / 1000.0) * fps
            
            # Predict the future volume based strictly on the KF's current velocity state
            predicted_vol = current_vol + (vol_rate * frames_ahead)
            
            if predicted_vol >= target_volume:
                self.pump_signal.emit(channel, 0.0)
                print(f"DEPOSIT COMPLETE: Predicted {predicted_vol:.2f} pL >= Target {target_volume} pL. Pressure zeroed.")
                break
            
            # Wait for next volume update (with 50ms timeout as fallback)
            with QMutexLocker(volume_mutex):
                volume_cond.wait(volume_mutex, 50)

    def _validate_deposit_preconditions(self, channel, pressure, target_volume):
        """Check all preconditions before starting a deposit. Returns (ok, msg)."""
        mw = self.main_window
        checks = [
            (mw.camera_status.isChecked(), "Camera not connected"),
            (hasattr(mw, 'arduino_controller') and mw.arduino_controller.is_connected, "Arduino not connected"),
            (mw.pumps_found, "Pumps not found"),
            (mw.controller.get_pressure(channel) >= 0, f"Pump {channel+1} pressure read failed"),
            (target_volume > 0, "Target volume must be > 0"),
            (hasattr(mw, 'model_thread') and mw.model_thread and mw.model_thread.isRunning(), "Model not running"),
            (mw.feedframes_chkbox.isChecked(), "Model feed disabled"),
        ]
        for ok, msg in checks:
            if not ok:
                return False, msg
        return True, "OK"

    def stop_script(self):
        if self.running:
            print("Stopping script...")
            with QMutexLocker(self.controller_mutex):
                self.running = False
        else:
            print("No script is currently running!")

    def stop(self):
        self.running = False
        with QMutexLocker(self.controller_mutex):
            self._script_pending = False
        self.quit()
        self.wait()

class ArduinoController(QObject):
    position_updated = Signal(int, int, int, int, int, int, float, float, float, float, float, float) 
    limits_updated = Signal(int, int, int) 
    connection_status_changed = Signal(bool, str) 

    def __init__(self, parent=None):
        super().__init__(parent)
        self.serial = QSerialPort(self)

        self.buffer = b''
        self.com_port_name = ""
        self.is_connected = False
        
        self.latest_x = 0
        self.latest_y = 0
        self.latest_z = 0
        self.latest_xs = 0
        self.latest_ys = 0
        self.latest_zs = 0
        
        self.latest_xspd = 0.0
        self.latest_yspd = 0.0
        self.latest_zspd = 0.0
        self.latest_xacc = 0.0
        self.latest_yacc = 0.0
        self.latest_zacc = 0.0
        
        self.latest_arduino_time = 0

        # Bind events
        self.serial.readyRead.connect(self._read_serial_data)
        self.serial.errorOccurred.connect(self._handle_error)

    @Slot(QSerialPort.SerialPortError)
    def _handle_error(self, error):
        # Triggered immediately if the USB cable is yanked physically
        if error == QSerialPort.ResourceError: # type: ignore
            print("ArduinoController: Hardware disconnected!")
            self.close()

    @Slot()
    def _read_serial_data(self):
        try:
            incoming_data = self.serial.readAll().data()
            if not incoming_data:
                return
                
            self.buffer += incoming_data
            
            while b'\n' in self.buffer:
                line, self.buffer = self.buffer.split(b'\n', 1)
                decoded_data = line.decode('utf_8', errors='ignore').strip()
                
                if decoded_data.startswith("P:"):
                    try:
                        parts = decoded_data.split(':')
                        # Format: P:X:Y:Z:Xs:Ys:Zs:Xspd:Yspd:Zspd:Xacc:Yacc:Zacc:Timestamp
                        if len(parts) == 14:
                            self.latest_x = int(parts[1])
                            self.latest_y = int(parts[2])
                            self.latest_z = int(parts[3])
                            self.latest_xs = int(parts[4])
                            self.latest_ys = int(parts[5])
                            self.latest_zs = int(parts[6])
                            
                            self.latest_xspd = float(parts[7])
                            self.latest_yspd = float(parts[8])
                            self.latest_zspd = float(parts[9])
                            self.latest_xacc = float(parts[10])
                            self.latest_yacc = float(parts[11])
                            self.latest_zacc = float(parts[12])
                            
                            self.latest_arduino_time = int(parts[13])
                            
                            self.position_updated.emit(
                                self.latest_x, self.latest_y, self.latest_z,
                                self.latest_xs, self.latest_ys, self.latest_zs,
                                self.latest_xspd, self.latest_yspd, self.latest_zspd,
                                self.latest_xacc, self.latest_yacc, self.latest_zacc
                            )
                    except ValueError as e:
                        print(f"ArduinoController: Error parsing coordinates: {decoded_data} - {e}")
                elif decoded_data.startswith("L"):
                    limits = decoded_data[1:].split(';')
                    if len(limits) == 3:
                        try:
                            l = int(float(limits[0]))
                            w = int(float(limits[1]))
                            h = int(float(limits[2]))
                            self.limits_updated.emit(l, w, h)
                        except ValueError:
                            print(f"ArduinoController: Error parsing limits: {decoded_data}")
        except Exception as e:
            print(f"ArduinoController: Error reading serial data: {e}")
            self.close()

    def connect(self) -> bool: # type: ignore
        ports = QSerialPortInfo.availablePorts()
        found_arduino = False
        
        print("\n--- Scanning for Arduino ---")
        for port in ports:
            desc = port.description().lower()
            vid = port.vendorIdentifier()
            pid = port.productIdentifier()
            print(f"Found Port: {port.portName()} | Desc: '{desc}' | VID: {vid} | PID: {pid}")
            
            if ("arduino" in desc or "ch340" in desc or "usb serial device" in desc or 
                "cp210" in desc or "ftdi" in desc or vid == 0x2341):
                
                self.com_port_name = port.portName()
                self.serial.setPortName(self.com_port_name)
                found_arduino = True
                print(f"-> Selected {self.com_port_name} as Arduino!\n")
                break

        if not found_arduino:
            print("-> No matching Arduino found.\n")
            self.connection_status_changed.emit(False, "No Arduino found.")
            self.is_connected = False
            return False

        if self.serial.isOpen():
            self.serial.close() 

        # Assign baud rate parameters right before opening 
        self.serial.setBaudRate(QSerialPort.Baud115200) # type: ignore
        self.serial.setDataBits(QSerialPort.Data8) # type: ignore
        self.serial.setParity(QSerialPort.NoParity) # type: ignore
        self.serial.setStopBits(QSerialPort.OneStop) # type: ignore
        self.serial.setFlowControl(QSerialPort.NoFlowControl) # type: ignore

        try:
            if self.serial.open(QIODevice.ReadWrite): # type: ignore
                self.is_connected = True
                self.serial.setDataTerminalReady(True)
                
                self.connection_status_changed.emit(True, f"Connected to Arduino on {self.com_port_name}")
                
                # Initialize Arduino dynamically (Start stream and get Limits)
                QTimer.singleShot(2000, lambda: self.send_command("S\n"))
                QTimer.singleShot(2100, lambda: self.send_command("L\n"))
                return True
            else:
                self.is_connected = False
                self.connection_status_changed.emit(False, f"Failed to open port {self.com_port_name}: {self.serial.errorString()}")
                return False
        except Exception as e:
            self.is_connected = False
            self.connection_status_changed.emit(False, f"Error connecting to Arduino: {e}")
            return False

    def send_command(self, command: str):
        if self.is_connected and self.serial.isOpen():
            try:
                self.serial.write(command.encode('utf-8'))
            except Exception as e:
                print(f"ArduinoController: Error sending command '{command.strip()}': {e}")
                self.close()

    def close(self):
        if self.serial.isOpen():
            self.serial.close()
        self.is_connected = False
        self.connection_status_changed.emit(False, "Arduino disconnected.")
        print(f"ArduinoController: Closed port: {self.com_port_name}")