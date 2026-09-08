from PySide6.QtCore import QThread, Signal, Slot, QMutex, QMutexLocker, QObject, QWaitCondition
from pypylon import pylon as py
import numpy as np
import cv2
import time
import subprocess

class videoSaver(QObject):
    progress_update = Signal(int)
    writer_released = Signal()

    def __init__(self):
        super().__init__()
        self.out = None
        self.written_count = 0
        self.compress = False

        self.cached_mask = None
        self.cache_mutex = QMutex()

    @Slot(object)
    def updateCache(self, frame):
        """Receives the latest mask from the Model Thread (~100Hz)"""
        with QMutexLocker(self.cache_mutex):
            self.cached_mask = frame

    @Slot()
    def writeFromCache(self):
        """Triggered by the Camera Thread (160Hz) to maintain video sync"""
        with QMutexLocker(self.cache_mutex):
            mask_to_write = self.cached_mask
        if mask_to_write is not None:
            self.saveFrame(mask_to_write)

    @Slot(str, int, tuple, bool, bool)
    def startWriter(self, filepath, fps, frame_size, is_16bit, compress):
        self.written_count = 0
        self.compress = compress
        width, height = frame_size

        # Define input pixel format based on your camera's active bit depth
        in_pix_fmt = 'gray16le' if is_16bit else 'gray'

        cmd = [
            r'./ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe',
            '-y',                        # Overwrite output files
            '-f', 'rawvideo',            # Input format
            '-vcodec', 'rawvideo',
            '-s', f'{width}x{height}',   # Frame size
            '-pix_fmt', in_pix_fmt,      # Raw input pixel format
            '-r', str(fps),              # Framerate
            '-i', '-',                   # Read from stdin
        ]

        if compress:
            # GPU Accelerated HEVC (10-bit to preserve dynamic range if 16-bit input)
            out_pix_fmt = 'p010le' if is_16bit else 'nv12'
            cmd.extend([
                '-c:v', 'hevc_nvenc',    # NVIDIA HEVC encoder
                '-preset', 'p6',         # Speed/Quality tradeoff (p1-p7)
                '-tune', 'hq',
                '-pix_fmt', out_pix_fmt
            ])
        else:
            # Lossless FFV1 (keeps native 16-bit grayscale without RGB bloat)
            cmd.extend([
                '-c:v', 'ffv1',
                '-level', '3',
                '-pix_fmt', in_pix_fmt
            ])

        cmd.append(filepath)

        # Launch subprocess
        self.process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    @Slot(object)
    def saveFrame(self, frame):
        if hasattr(self, 'process') and self.process.poll() is None:
            try:
                # Pipe raw numpy bytes directly to ffmpeg
                self.process.stdin.write(frame.tobytes())
                self.written_count += 1
                self.progress_update.emit(self.written_count)
            except Exception as e:
                print(f"Saver error: {e}")

    @Slot()
    def releaseWriter(self):
        was_writing = False
        
        # FFmpeg process cleanup (for the main camera)
        if hasattr(self, 'process') and self.process is not None:
            if self.process.poll() is None:
                try:
                    self.process.stdin.close()
                except Exception:
                    pass
                self.process.wait()
            self.process = None
            was_writing = True
            
        # OpenCV VideoWriter fallback (for your mask saver)
        if getattr(self, 'out', None) is not None:
            self.out.release()
            self.out = None
            was_writing = True

        # Only tell the UI a file finished if we actually closed one
        if was_writing:
            self.writer_released.emit()

class captureCamera(QThread):
    timestamp = Signal(float)
    frame_out = Signal(object) 
    frame_out_for_model = Signal(object)
    display_out = Signal(tuple)
    start_record_out = Signal(str, int, tuple, bool, bool)
    release_out = Signal() 
    mask_sync_trigger = Signal()

    record_progress = Signal(int, int)
    record_finished = Signal()

    def __init__(self, camera=None, fps=160, name='a2A1920-160umBAS', tlf=py.TlFactory.GetInstance()):
        super().__init__()
        if camera is None:
            try:
                py.TlFactory.GetInstance().EnumerateDevices()[0]
            except:
                print("No pylon cameras detected!")
        self.running = True
        self.desired_fps = fps
        self.name = name
        self.tlf = tlf
        self.cameraDevice = camera
        self.exposure=100
        self.frame_size=(1920, 1200)
        self.record=False
        self.camera=None
        self.start_time = time.perf_counter()
        self.latest_frame_time = 0.0
        self.frames_captured = 0 # Track total frames
        self.frames_dropped = 0  # Track dropped frames
        self.frame_id = 0        # Monotonic frame ID for pipeline integrity
        self.watchdog = None     # Reference to DeviceWatchdog (set externally)

        # video saver thread
        self.saver_thread = QThread()
        self.saver = videoSaver()
        self.saver.moveToThread(self.saver_thread)
        self.saver_thread.start()
        self.take_screenshot_flag = False
        self.screenshot_path = ""
        
        # Connect strict-type signals
        self.start_record_out.connect(self.saver.startWriter)
        self.frame_out.connect(self.saver.saveFrame)
        self.release_out.connect(self.saver.releaseWriter)
        
        # Connect the new progress trackers
        self.saver.progress_update.connect(self._handle_saver_progress)
        self.saver.writer_released.connect(self.record_finished)

        self.param_mutex = QMutex()
        self.pending_params = {}
        self.limits = {}
        self.current_vals = {}       

        self.last_display_time = 0.0
        self.display_interval = 1.0 / 30.0
        self.last_timestamp = time.perf_counter()
        self.actual_fps = 0.0

        try:
            self.camera = py.InstantCamera(self.tlf.CreateDevice(self.cameraDevice)) 
            if self.camera is not None:
                self.camera.Open()

                self.camera.PixelFormat.Value = "Mono12p"
                self.camera.ExposureAuto.Value = "Off"
                self.camera.Gain.Value = 0
                self.camera.ExposureTime.Value=100
                max_exposure = min(33333, self.camera.ExposureTime.Max) 
                
                self.camera.AcquisitionFrameRateEnable.Value = False
                self.camera.AcquisitionFrameRate.Value = 1000
                self.camera.DeviceLinkThroughputLimitMode.SetValue("On")
                self.camera.DeviceLinkThroughputLimit.SetValue(419000000)
                current_limit = self.camera.DeviceLinkThroughputLimit.GetValue()
                print(f"Bandwidth set to: {current_limit / 1000000} MB/s")

                self.limits = {
                    "exposure": (self.camera.ExposureTime.Min, max_exposure),
                    "gain": (self.camera.Gain.Min, self.camera.Gain.Max),
                    "width": (self.camera.Width.Min, self.camera.Width.Max),
                    "height": (self.camera.Height.Min, self.camera.Height.Max)
                }
                is_12_bit = self.camera.PixelFormat.Value in ["Mono12", "Mono12p", "Mono12Packed"]
                self.is_16bit = is_12_bit
                self.current_vals = {
                    "exposure": self.camera.ExposureTime.Value,
                    "gain": self.camera.Gain.Value,
                    "width": self.camera.Width.Value,
                    "height": self.camera.Height.Value,
                    "dynamic_range": 0 if is_12_bit else 1
                }
            else:
                print("No camera object!")
        except Exception as e:
            print(f"Invalid camera object: {e}")
        
        self.frame_duration = 1.0 / self.desired_fps

    @Slot(int)
    def _handle_saver_progress(self, written):
        # Only broadcast progress to the UI if we are in the "draining" phase (post-recording)
        if not self.record and self.frames_captured > 0:
            self.record_progress.emit(written, self.frames_captured)

    @Slot(object, float, float, bool, int)
    def _dispatch_frames(self, processed_frame, fps, timestamp, record, frame_id):
        """Emits frame to model (with frame_id) and throttled display."""
        self.frame_out_for_model.emit(processed_frame)

        current_time = time.perf_counter()

        delta = current_time - self.last_timestamp
        if delta > 0:
            inst_fps = 1.0 / delta
            self.actual_fps = (self.actual_fps * 0.7) + (inst_fps * 0.3)
        else:
            self.actual_fps = 0.0
            
        self.last_timestamp = current_time

        if current_time - self.last_display_time >= self.display_interval:
            self.display_out.emit((processed_frame, fps, self.actual_fps, timestamp, record))
            self.last_display_time = current_time

        # Watchdog heartbeat
        if self.watchdog is not None:
            self.watchdog.heartbeat("camera", {"frame_id": frame_id})

    @Slot(str)
    def takeScreenshot(self, filepath):
        with QMutexLocker(self.param_mutex):
            self.screenshot_path = filepath
            self.take_screenshot_flag = True

    @Slot(bool)
    def setClaheEnabled(self, enabled):
        # CLAHE now handled in model thread; forwarded via param_mutex
        with QMutexLocker(self.param_mutex):
            self.pending_params['clahe_enabled'] = enabled

    @Slot(float, int)
    def updateClaheParams(self, clip_limit, tile_grid):
        with QMutexLocker(self.param_mutex):
            self.pending_params['clahe_clip'] = clip_limit
            self.pending_params['clahe_grid'] = tile_grid

    @Slot(int)
    def setExposure(self, val):
        with QMutexLocker(self.param_mutex):
            self.pending_params['exposure'] = val

    @Slot(int)
    def setGain(self, val):
        with QMutexLocker(self.param_mutex):
            self.pending_params['gain'] = val

    @Slot(int)
    def setWidth(self, val):
        with QMutexLocker(self.param_mutex):
            self.pending_params['width'] = val

    @Slot(int)
    def setHeight(self, val):
        with QMutexLocker(self.param_mutex):
            self.pending_params['height'] = val

    @Slot(int)
    def setDynamicRange(self, idx):
        with QMutexLocker(self.param_mutex):
            self.pending_params['dynamic_range'] = idx

    def startCamera(self):
        if self.camera is not None:
            print(f"Starting frame collection: {self.name}")
            self.camera.StartGrabbing(py.GrabStrategy_LatestImageOnly)
        else:
            print(f"No camera object found: {self.camera}")

    def stopCamera(self):
        self.camera.StopGrabbing()
        
    def run(self):
        camera = self.camera
        previous_frame = None
        converter = py.ImageFormatConverter()
        converter.OutputPixelFormat = py.PixelType_Mono16
        converter.OutputBitAlignment = py.OutputBitAlignment_MsbAligned
        while self.running and camera is not None:
            with QMutexLocker(self.param_mutex):
                if self.pending_params:
                    needs_stop = 'width' in self.pending_params or 'height' in self.pending_params or 'dynamic_range' in self.pending_params
                    was_grabbing = camera.IsGrabbing()

                    if needs_stop and was_grabbing:
                        camera.StopGrabbing()
                    
                    try:
                        if 'dynamic_range' in self.pending_params:
                            idx = self.pending_params['dynamic_range']
                            if idx == 0: 
                                try:
                                    camera.PixelFormat.Value = "Mono12p" 
                                except:
                                    camera.PixelFormat.Value = "Mono12"  
                                converter.OutputPixelFormat = py.PixelType_Mono16
                                self.is_16bit = True # User switched to 12-bit
                            elif idx == 1: 
                                camera.PixelFormat.Value = "Mono8"
                                converter.OutputPixelFormat = py.PixelType_Mono8
                                self.is_16bit = False # User switched to 8-bit
                        if 'exposure' in self.pending_params:
                            camera.ExposureTime.Value = float(self.pending_params['exposure'])
                        if 'gain' in self.pending_params:
                            camera.Gain.Value = float(self.pending_params['gain'])
                        if 'width' in self.pending_params:
                            inc = getattr(camera.Width, 'Inc', 2) 
                            camera.Width.Value = int(self.pending_params['width'] // inc) * inc
                        if 'height' in self.pending_params:
                            inc = getattr(camera.Height, 'Inc', 2)
                            camera.Height.Value = int(self.pending_params['height'] // inc) * inc
                            
                        self.frame_size = (camera.Width.Value, camera.Height.Value)
                    except Exception as e:
                        print(f"Failed to update camera parameters: {e}")

                    self.pending_params.clear()

                    if needs_stop and was_grabbing:
                        camera.StartGrabbing(py.GrabStrategy_LatestImageOnly)
            try:
                if camera.IsGrabbing():
                    grabResult = camera.RetrieveResult(5000, py.TimeoutHandling_ThrowException)
                    
                    if grabResult and grabResult.IsValid():
                        if grabResult.GrabSucceeded():
                            image = converter.Convert(grabResult)
                            frame = image.GetArray()
                            if previous_frame is None:
                                previous_frame = frame.copy()
                            
                            current_fps = camera.ResultingFrameRate.Value

                            if frame is None or frame.size == 0:
                                print("Invalid frame received! Passing previous.")
                                frame = previous_frame
                            else:
                                previous_frame = frame.copy()
                            
                            self.latest_frame_time = time.perf_counter() - self.start_time

                            with QMutexLocker(self.param_mutex):
                                if getattr(self, 'take_screenshot_flag', False):
                                    try:
                                        cv2.imwrite(f'{self.screenshot_path}_{self.latest_frame_time}.tiff', frame)
                                        print(f"Screenshot saved: {self.screenshot_path}_{self.latest_frame_time}")
                                    except Exception as e:
                                        print(f"Failed to save screenshot: {e}")
                                    self.take_screenshot_flag = False


                            self.frame_id += 1

                            # Convert 16-bit to 8-bit inline (CLAHE done in model thread)
                            if frame.dtype == np.uint16:
                                out_frame = (frame >> 8).astype(np.uint8)
                            else:
                                out_frame = frame.astype(np.uint8)

                            if self.record:
                                self.frames_captured += 1
                                self.frame_out.emit(out_frame.copy())
                                self.timestamp.emit(self.latest_frame_time)
                                self.mask_sync_trigger.emit()

                            self._dispatch_frames(out_frame, current_fps, self.latest_frame_time, self.record, self.frame_id)
                        
                        grabResult.Release()
                            
            except py.TimeoutException:
                pass # Safe to ignore timeouts
            except Exception as e:
                err_msg = str(e)
                # If we are stopping and grab is cancelled, exit cleanly
                if not self.running and "No grab result data is referenced" in err_msg:
                    break 
                    
                print(f"Error grabbing frames: {err_msg}")
                if "A device which does not exist" in err_msg or "Device has been removed" in err_msg:
                    print("Camera disconnected! Killing thread.")
                    self.stop()
                break

        # SHUTDOWN SEQUENCE
        self.release_out.emit()
        time.sleep(0.1) # Yield momentarily to allow signal propagation to backend thread

        if hasattr(self, 'saver_thread') and self.saver_thread.isRunning():
            self.saver_thread.quit()
            self.saver_thread.wait()

        try:
            if self.camera is not None and self.camera.IsOpen():
                self.camera.Close()
        except: pass

    def startRecord(self, filename, save_directory, compress=False):
        self.release_out.emit()
        self.frames_captured = 0
        
        is_16bit = getattr(self, 'is_16bit', False)
        # STRICTLY enforce .mkv container for FFV1 compatibility universally
        ext = '.mkv'
        full_path = f"{save_directory}/{filename}{ext}"
        
        # Dispatch to background thread
        self.start_record_out.emit(full_path, self.desired_fps, self.frame_size, is_16bit, compress)

        self.start_time = time.perf_counter()
        self.record = True

    def stopRecord(self):
        self.record = False
        self.release_out.emit()
    
    def stop(self):
        self.record = False
        self.running = False
        
        # Stop grabbing to unblock RetrieveResult immediately
        try:
            if self.camera is not None and self.camera.IsGrabbing():
                self.camera.StopGrabbing()
        except: pass
            
        self.quit()
        if QThread.currentThread() != self:
            self.wait()