# Architecture Overview

## Threading Model

The application uses Qt's QThread system with worker objects to keep the UI responsive:

```
┌─────────────────────────────────────────────────────┐
│                    Main Thread                       │
│  MainWindow (QMainWindow)                            │
│  - UI updates, signal/slot dispatch                  │
│  - Timer-driven pump polling (update_pump_info)      │
│  - Keyboard/mouse event handling                     │
└──────────────┬──────────────────┬───────────────────┘
               │                  │
               ▼                  ▼
    ┌──────────────────┐  ┌──────────────────┐
    │  cameraThread    │  │  modelThread     │
    │ (QThread)        │  │ (QThread)        │
    │                  │  │                  │
    │ captureCamera    │  │ runModel (QObj)  │
    │ - Basler frame   │  │ - YOLO inference │
    │   acquisition    │  │ - Kalman filter  │
    │ - Dispatching    │  │                  │
    └──────────────────┘  └──────────────────┘
               │                  │
               ▼                  ▼
         ┌──────────────────────────┐
         │   scriptRunner (QThread) │
         │   - JSON script playback │
         │   - Stage movement cmds  │
         │   - Pressure setpoints   │
         └──────────────────────────┘
```

### Frame Pipeline

1. **Camera thread** captures frame from Basler camera
2. Frame dispatched to **model thread** via signal (`dispatchFrame`)
3. Model thread runs YOLO inference → bounding boxes + masks
4. Kalman filter optionally smooths predictions
5. Results emitted back to main thread via signals
6. Main thread renders overlay on camera_label

## Key Classes

| Class | File | Role |
|-------|------|------|
| `MainWindow` | `main.py` | Application entry, UI setup, signal wiring |
| `captureCamera` | `camera.py` | Basler camera acquisition in QThread |
| `runModel` | `model.py` | YOLO inference worker, Kalman filter |
| `FluigentController` | `utils.py` | Fluigent SDK wrapper (pressure control) |
| `ArduinoController` | `utils.py` | Serial communication with stage |
| `scriptRunner` | `utils.py` | Playback of JSON experimental scripts |
| `DeviceWatchdog` | `watchdog.py` | USB hotplug monitoring |
| `SessionLogger` | `session_logger.py` | CSV data recording |

## Signal Flow

```
cameraThread ──dispatchFrame──▶ modelThread ──modelResult──▶ MainWindow
                                     │                          │
                                     │ (Kalman predict/correct)  │
                                     │                          ▼
                                                      camera_label.update()
                                                      (overlay draw)
```

## Model Configuration

All model parameters are set at the class level in `model.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `conf_threshold` | 0.5 | Detection confidence threshold |
| `iou_threshold` | 0.5 | NMS IoU threshold |
| `max_det` | 300 | Maximum detections per frame |
| `clahe_enabled` | False | Adaptive histogram equalization |
| `kalman_enabled` | False | Kalman filter smoothing |

The model uses **GPU if available** (`cuda:0`), otherwise **CPU** with automatic fallback.