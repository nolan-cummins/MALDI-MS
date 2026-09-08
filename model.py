from PySide6.QtCore import QThread, Signal, Slot, QMutex, QMutexLocker, QWaitCondition, QObject, QCoreApplication
from ultralytics import YOLO
import cv2
import numpy as np
import time
from numba import njit

def get_iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    return interArea / float(boxAArea + boxBArea - interArea + 1e-6)

@njit(fastmath=True)
def _numba_volume_loop(region, poly_coeffs):
    vol_px3 = 0.0
    rows, cols = region.shape
    
    for y in range(rows):
        # Numba-compatible way to find the first and last active pixel in the row
        row_pixels = np.where(region[y, :])[0]
        if len(row_pixels) == 0:
            continue
            
        mean_x = np.mean(row_pixels)
        
        # Calculate midline boundary based on polynomial coefficients (z_poly)
        boundary_y = poly_coeffs[0] * mean_x + poly_coeffs[1]
        if y > boundary_y:
            continue
            
        radius = (row_pixels[-1] - row_pixels[0]) / 2.0
        vol_px3 += np.pi * (radius ** 2)
        
    return vol_px3

def calculate_volume(binary_mask, px_um):
    rows = np.any(binary_mask, axis=1)
    if not np.any(rows): return 0.0
    
    y_idx, x_idx = np.where(binary_mask)
    ymin, ymax, xmin, xmax = y_idx.min(), y_idx.max(), x_idx.min(), x_idx.max()
    region = binary_mask[ymin:ymax+1, xmin:xmax+1]
    y_r, x_r = np.where(region)
    
    # Fit poly to find midline for rotation (Numpy handles this fine)
    col_mids = [np.mean(np.where(region[:, c])[0]) for c in np.unique(x_r)]
    z_poly = np.polyfit(np.unique(x_r), col_mids, 1)
    
    # 3. Pass the data to the pre-compiled Numba function
    vol_px3 = _numba_volume_loop(region, z_poly)
    
    return (vol_px3 * (px_um**3)) / 1000.0, vol_px3

class runModel(QObject):
    frame_out = Signal(tuple)
    time_out = Signal(tuple)
    volume_out = Signal(float, float, float)
    mask_record_out = Signal(object)

    def __init__(self, model_path='yolo/best.pt'):
        super().__init__()
        self.model = YOLO(model_path, task='segment')
        self.running = True
        # Warmup: use CUDA if available, else CPU
        import torch
        _device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.model.predict(np.zeros((640, 640, 3), dtype=np.uint8), imgsz=640, device=_device) # Warmup

        # Settings mutex
        self.settings = {
            'confidence': 0.5,
            'px_um': 0.531447395, # Default pixel-to-micron conversion at 20x, 0.3776319968 for 10x
            'ema_enabled': False,
            'fit_ellipse': False,
            'clahe_enabled': False,
            'clahe_clip': 2.0,
            'clahe_grid': 8,
        }
        self.settings_mutex = QMutex()
        self.feed = True
        
        # Frame buffering and condition variable
        self.frame_mutex = QMutex()
        self.cond = QWaitCondition()
        self.latest_frame = None
        self.latest_frame_id = 0
        self.frame_queue_count = 0
        self.last_ui_update_time = 0.0

        # CLAHE preprocessor (applied to Mono8 before GRAY2BGR)
        self.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

        # Error resilience counters
        self.error_count = 0
        self.last_error = ""
        self.max_inference_hz = 60      # Target inference rate
        self.last_inference_time = 0.0  # For throttling
        self.total_model_dropped = 0
        self.watchdog = None            # Reference to DeviceWatchdog (set externally)

        # KF Configuration (Constant Velocity Model)
        self.kf = cv2.KalmanFilter(8, 4)
        self.kf.transitionMatrix = np.eye(8, dtype=np.float32)
        for i in range(4): self.kf.transitionMatrix[i, i+4] = 1 
        self.kf.measurementMatrix = np.eye(4, 8, dtype=np.float32)
        
        self.kf.processNoiseCov = np.eye(8, dtype=np.float32) * 1e-4
        self.kf.measurementNoiseCov = np.eye(4, dtype=np.float32) * 1e-2
        
        # Tracking Logic State
        self.initialized = False
        self.patience_ms = 500.0 
        self.iou_threshold = 0.5
        self.history_boxes = [] # Stores [x1, y1, x2, y2] for IoU checks
        self.last_valid_mask = None
        self.last_valid_box = None
        self.last_valid_time = 0.0 # Time of last real YOLO detection
        self.missed_frames_count = 0
        self.missed_limit = 5     # Increased to match the new script logic
        self.history_limit = 30

        # Volume Interpolation State
        self.prev_area = None     # Stores last valid box area (w * h)
        self.last_vol = 0.0       # Stores last calculated volume (pL)

        # Numba JIT compilation
        dummy_region = np.ones((10, 10), dtype=bool)
        dummy_poly = np.array([1.0, 1.0], dtype=np.float64)
        _numba_volume_loop(dummy_region, dummy_poly)

        # Cropping
        self.crop_coords = None
        self.crop_mutex = QMutex()

    @Slot(tuple)
    def updateCrop(self, crop_tuple):
        """Asynchronously receive crop offsets from the Main GUI"""
        with QMutexLocker(self.crop_mutex):
            self.crop_coords = crop_tuple

    @Slot(float)
    def setPatience(self, val_ms):
        with QMutexLocker(self.settings_mutex):
            self.settings['patience'] = val_ms

    @Slot(float)
    def updateConfidence(self, conf_level):
        with QMutexLocker(self.settings_mutex):
            self.settings['confidence'] = conf_level

    @Slot(bool)
    def setClaheEnabled(self, enabled):
        with QMutexLocker(self.settings_mutex):
            self.settings['clahe_enabled'] = enabled

    @Slot(float, int)
    def updateClaheParams(self, clip_limit, tile_grid):
        with QMutexLocker(self.settings_mutex):
            self.settings['clahe_clip'] = clip_limit
            self.settings['clahe_grid'] = tile_grid
        # Rebuild CLAHE object outside the mutex to avoid blocking
        self.clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_grid, tile_grid))

    @Slot(float)
    def setPxUm(self, val):
        with QMutexLocker(self.settings_mutex):
            self.settings['px_um'] = val

    @Slot(bool)
    def feedModel(self, feed):
        with QMutexLocker(self.frame_mutex):
            self.feed = feed

    @Slot(object)
    def receiveFrame(self, frame):
        with QMutexLocker(self.frame_mutex):
            if self.feed:
                self.latest_frame = frame
                self.frame_queue_count += 1
                self.cond.wakeOne()
            else:
                self.latest_frame = None

    @Slot(bool)
    def setEmaEnabled(self, enabled):
        with QMutexLocker(self.settings_mutex):
            self.settings['ema_enabled'] = enabled

    @Slot(bool)
    def setFitEllipseEnabled(self, enabled):
        with QMutexLocker(self.settings_mutex):
            self.settings['fit_ellipse'] = enabled

    def run(self):
        while self.running:
            #QCoreApplication.processEvents()
            with QMutexLocker(self.frame_mutex):
                while self.latest_frame is None and self.running:
                    self.cond.wait(self.frame_mutex)
                if not self.running: break
                frame = self.latest_frame
                self.latest_frame = None
                frame_delay = max(0, self.frame_queue_count - 1)
                self.frame_queue_count = 0 

            with QMutexLocker(self.settings_mutex):
                conf = self.settings['confidence']
                px_um = self.settings['px_um']
                ema_enabled = self.settings['ema_enabled']
                fit_ellipse = self.settings['fit_ellipse']
                clahe_enabled = self.settings.get('clahe_enabled', False)
                clahe_clip = self.settings.get('clahe_clip', 2.0)
                clahe_grid = self.settings.get('clahe_grid', 8)

            if frame is not None:
                try:
                    current_time = time.perf_counter()
                    
                    # 1. Thread-safe crop fetching
                    with QMutexLocker(self.crop_mutex):
                        crop_coords = self.crop_coords
                    
                    full_h, full_w = frame.shape[:2]
                    cx, cy, cw, ch = 0, 0, full_w, full_h
                    if crop_coords is not None:
                        cx, cy, cw, ch = crop_coords
                        
                    # 2. CLAHE preprocessing (on Mono8 frame before GRAY2BGR)
                    if len(frame.shape) == 2:
                        if clahe_enabled:
                            frame = self.clahe.apply(frame)
                        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
                    cropped_frame = frame[cy:cy+ch, cx:cx+cw]

                    # 3. Advance the Kalman Filter
                    
                    # 2. Run YOLO
                    import torch
                    _device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
                    results = self.model.predict(
                        cropped_frame, 
                        imgsz=640, 
                        conf=conf, 
                        verbose=False, 
                        device=_device,
                        half=torch.cuda.is_available(),  # FP16 only on GPU
                        augment=False,    # Guarantee Test-Time Augmentation is off
                        agnostic_nms=True # Faster NMS if you only have 1 class (droplet)
                    )
                    result = results[0]
                    m_boxes = result.boxes.xyxy.cpu().numpy() if result.boxes is not None else []
                    
                    valid_detection = False
                    det_box = None

                    if len(m_boxes) > 0:
                        det_box = m_boxes[0]
                        # Only apply IOU gate if we already have a tracking history
                        # if self.initialized and self.history_boxes:
                        #     ref_box = self.history_boxes[-1]
                        #     if get_iou(det_box, ref_box) >= self.iou_threshold:
                        #         valid_detection = True
                        # else:
                        #     # Trust the first detection after a reset
                        #     valid_detection = True

                    # 3. State Machine Logic
                    if det_box is not None: # removed IOU check for fast initial growth
                        self.last_valid_time = current_time
                        self.missed_frames_count = 0
                        
                        x1, y1, x2, y2 = det_box
                        w, h = x2 - x1, y2 - y1
                        box_cx, box_cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0
                        meas = np.array([[box_cx], [box_cy], [w], [h]], np.float32)

                        if not self.initialized:
                            # PREVENT JUMP: Sync statePre and statePost immediately
                            self.kf.statePre = np.zeros((8, 1), np.float32)
                            self.kf.statePost = np.zeros((8, 1), np.float32)
                            self.kf.statePre[:4], self.kf.statePost[:4] = meas, meas
                            self.initialized = True
                            prediction = self.kf.statePre.copy()  # Use current state as initial prediction
                        else:
                            prediction = self.kf.predict()  # Advance filter
                            self.kf.correct(meas)  # Correct with measurement

                        # Volume and Mask Processing
                        full_mask = np.zeros((ch, cw), dtype=np.uint8)
                        
                        if fit_ellipse:
                            x1, y1, x2, y2 = map(int, det_box)
                            center = ((x1 + x2) // 2, (y1 + y2) // 2)
                            axes = (max(1, (x2 - x1) // 2), max(1, (y2 - y1) // 2))
                            cv2.ellipse(full_mask, center, axes, 0, 0, 360, 1, -1)
                        else:
                            if result.masks is not None and len(result.masks.xy) > 0:
                                poly = result.masks.xy[0].astype(np.int32)
                                if len(poly) > 0:
                                    cv2.fillPoly(full_mask, [poly], 1)

                        record_mask = np.zeros((full_h, full_w), dtype=np.uint8)
                        record_mask[cy:cy+ch, cx:cx+cw] = (full_mask * 255).astype(np.uint8)
                        self.mask_record_out.emit(record_mask)
                            
                        vol_pl, vol_px3 = calculate_volume(full_mask > 0.5, px_um)

                        # EMA Smoothing
                        if ema_enabled and self.initialized:
                            alpha = 0.8
                            self.ema_vol_pl = alpha * vol_pl + (1 - alpha) * getattr(self, 'ema_vol_pl', vol_pl)
                            self.ema_vol_px3 = alpha * vol_px3 + (1 - alpha) * getattr(self, 'ema_vol_px3', vol_px3)
                            
                            mask_f = full_mask.astype(np.float32)
                            if not hasattr(self, 'ema_mask') or self.ema_mask.shape != mask_f.shape:
                                self.ema_mask = mask_f
                            self.ema_mask = alpha * mask_f + (1 - alpha) * self.ema_mask
                            
                            if not hasattr(self, 'ema_box'):
                                self.ema_box = det_box.copy()
                            self.ema_box = alpha * det_box + (1 - alpha) * self.ema_box
                            
                            out_vol_pl = self.ema_vol_pl
                            out_vol_px3 = self.ema_vol_px3
                            out_mask = (self.ema_mask > 0.5).astype(np.uint8)
                            out_box = self.ema_box.copy()
                        else:
                            out_vol_pl = vol_pl
                            out_vol_px3 = vol_px3
                            out_mask = full_mask
                            out_box = det_box.copy() # Use raw box
                            
                            self.ema_vol_pl = vol_pl
                            self.ema_vol_px3 = vol_px3
                            self.ema_mask = full_mask.astype(np.float32)
                            self.ema_box = det_box.copy()

                        # KF Velocity-based rate prediction (pL/frame)
                        kf_w, kf_h = self.kf.statePost[2, 0], self.kf.statePost[3, 0]
                        kf_dw, kf_dh = self.kf.statePost[6, 0], self.kf.statePost[7, 0]
                        next_area = max(0, kf_w + kf_dw) * max(0, kf_h + kf_dh)
                        curr_area = max(1, kf_w * kf_h)
                        vol_rate = out_vol_pl * (next_area / curr_area) - out_vol_pl
                        
                        self.last_valid_mask, self.last_valid_box = out_mask, det_box
                        self.last_vol, self.prev_area = out_vol_pl, w * h
                        self.history_boxes.append(det_box)
                        
                        output = ([out_box], [out_mask], [result.boxes.conf[0].item()], out_vol_pl, vol_rate, out_vol_px3)

                    elif self.initialized and self.missed_frames_count < self.missed_limit:
                        # KALMAN INTERPOLATION MODE
                        time_since_last = (current_time - self.last_valid_time)
                        
                        # 1. Initialize an empty mask safely
                        record_mask = np.zeros((full_h, full_w), dtype=np.uint8) 
                        
                        if time_since_last < (self.patience_ms / 1000.0):
                            self.missed_frames_count += 1
                            pcx, pcy, pw, ph = prediction[:4].flatten()
                            
                            # Reconstruct box: [x1, y1, x2, y2]
                            kf_box = np.array([pcx - pw/2, pcy - ph/2, pcx + pw/2, pcy + ph/2])
                            
                            curr_area = pw * ph
                            comp_factor = curr_area / self.prev_area if self.prev_area else 1.0
                            vol_pl = self.last_vol * comp_factor
                            
                            # Reverse engineer px3 from pl using the current conversion factor
                            vol_px3 = (vol_pl * 1000.0) / (px_um**3)
                            
                            # Interpolation velocity fallback
                            kf_dw, kf_dh = self.kf.statePre[6, 0], self.kf.statePre[7, 0]
                            next_area = max(0, pw + kf_dw) * max(0, ph + kf_dh)
                            vol_rate = vol_pl * (next_area / max(1, curr_area)) - vol_pl
                            
                            # 2. Fix shape mismatch: fallback is now (ch, cw), not frame.shape
                            kf_mask = self._stretch_mask(self.last_valid_mask, self.last_valid_box, kf_box) if self.last_valid_mask is not None else np.zeros((ch, cw), dtype=np.uint8)

                            self.history_boxes.append(kf_box)
                            output = ([kf_box], [kf_mask], ["K"], vol_pl, vol_rate, vol_px3)
                            
                            # 3. Only apply kf_mask to the record_mask inside the 'if' block where it exists
                            if self.last_valid_mask is not None:
                                record_mask[cy:cy+ch, cx:cx+cw] = (kf_mask * 255).astype(np.uint8)
                        else:
                            self.reset_kf()
                            output = ([], [], [], 0.0, 0.0, 0.0)

                        # Emit the mask (will be empty if patience exceeded)
                        self.mask_record_out.emit(record_mask)

                    else:
                        # No detection AND not initialized yet: emit empty output
                        output = ([], [], [], 0.0, 0.0, 0.0)
                        record_mask = np.zeros((full_h, full_w), dtype=np.uint8)
                        self.mask_record_out.emit(record_mask)

                    # 4. Final Cleanup and Emission
                    if len(self.history_boxes) > self.history_limit: self.history_boxes.pop(0)
                    
                    current_time_ui = time.perf_counter()
                    if current_time_ui - self.last_ui_update_time >= 1.0 / 30.0:
                        self.last_ui_update_time = current_time_ui
                        self.frame_out.emit((np.array(output[0]), np.array(output[1]), output[2]))

                    self.time_out.emit((result.speed.get('inference', 0.0), result.speed.get('preprocess', 0.0), frame_delay))
                    self.volume_out.emit(output[3], output[4], output[5])
                    
                    # Watchdog heartbeat
                    if self.watchdog is not None:
                        self.watchdog.heartbeat("model", {"inference_ms": result.speed.get('inference', 0.0)})

                except Exception:
                    import traceback
                    self.error_count += 1
                    self.last_error = traceback.format_exc()
                    print("Error running inference:")
                    traceback.print_exc()
                    
                    # Emit empty results to keep UI from stale overlays
                    self.frame_out.emit((np.array([]), np.array([]), []))
                    self.volume_out.emit(0.0, 0.0, 0.0)
                    self.time_out.emit((0.0, 0.0, 0))
                    
                    if self.error_count > 10:
                        self.running = False
                        print("Model: too many errors, stopping thread")

    def reset_kf(self):
        self.kf = cv2.KalmanFilter(8, 4)
        self.kf.transitionMatrix = np.eye(8, dtype=np.float32) # Position only
        self.kf.measurementMatrix = np.eye(4, 8, dtype=np.float32)
        self.kf.processNoiseCov = np.eye(8, dtype=np.float32) * 1e-4
        self.kf.measurementNoiseCov = np.eye(4, dtype=np.float32) * 1e-3 # Trust YOLO more
        self.initialized = False

    def _stretch_mask(self, mask, old_box, new_box):
        """Stretches the mask to fit edge-to-edge in the new box."""
        w_old, h_old = max(1, old_box[2]-old_box[0]), max(1, old_box[3]-old_box[1])
        w_new, h_new = max(1, new_box[2]-new_box[0]), max(1, new_box[3]-new_box[1])
        
        sx, sy = w_new / w_old, h_new / h_old
        tx = new_box[0] - sx * old_box[0]
        ty = new_box[1] - sy * old_box[1]
        
        M = np.array([[sx, 0, tx], [0, sy, ty]], dtype=np.float32)
        return cv2.warpAffine(mask, M, (mask.shape[1], mask.shape[0]))

    def stop(self):
        self.running = False
        with QMutexLocker(self.frame_mutex):
            self.cond.wakeAll()