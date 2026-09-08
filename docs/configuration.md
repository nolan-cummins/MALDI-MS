# Configuration Reference

## config.json

The app loads `config.json` at startup. All fields are optional; missing keys use defaults.

```json
{
    "camera_exposure": 5000.0,
    "camera_gain": 1.0,
    "camera_gamma": 1.0,
    "target_fps": 60
}
```

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `camera_exposure` | float | 5000.0 | Exposure time in µs |
| `camera_gain` | float | 1.0 | Analog gain multiplier |
| `camera_gamma` | float | 1.0 | Gamma correction value |
| `target_fps` | int | 60 | Target frames per second |

## UI Controls

### Camera Panel
- **Start/Stop** — Toggle camera acquisition
- **FPS** — Target frames-per-second slider
- **Overlay** — Toggle timestamp/FPS/text overlay
- **Crop (C key)** — Press C, then click-drag to select ROI; release to crop

### Pump Panel
- **Setpoint sliders** — Target pressure per channel (mBar)
- **Zero** — Set pressure to 0
- **Calibrate** — Recalibrate pressure sensor
- **Status indicator** — Green = connected, Red = disconnected

### Model Panel
- **Start Model** — Begin YOLO inference on camera feed
- **Confidence** — Detection threshold slider (0.0 - 1.0)
- **CLAHE** — Enable adaptive histogram equalization
- **Kalman Filter** — Enable temporal smoothing
- **Feed Frames** — Toggle model overlay on camera view

### Script / Stage
- **Script selector** — Load and run JSON experiment scripts
- **X/Y/Z control** — Manual stage movement (mm or steps)
- **Home** — Return stage to origin

### Recording
- **Record** — Start/stop CSV data logging
- **Save directory** — Choose where recording CSVs are saved
- **Screenshot** — Capture current camera frame to file

## JSON Experiment Script Format

Scripts are JSON files with a list of commands:

```json
[
    {"set_pressure": [0, 2000.0]},
    {"sleep": 1.0},
    {"set_pressure": [1, 1500.0]},
    {"sleep": 0.5},
    {"move": [10, 20, 0]},
    {"sleep": 0.3},
    {"set_pressure": [0, 0]},
    {"set_pressure": [1, 0]}
]
```

### Commands
| Command | Parameters | Description |
|---------|------------|-------------|
| `set_pressure` | `[channel, mBar]` | Set pump channel pressure |
| `sleep` | `seconds` | Wait for duration |
| `move` | `[x, y, z]` | Move stage relative (mm) |
| `move_to` | `[x, y, z]` | Move stage absolute (mm) |
| `home` | — | Home all axes |
| `record_start` | — | Begin recording |
| `record_stop` | — | End recording |