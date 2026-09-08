# Hardware Setup

## Fluigent LineUP Pressure Controller

### Connections
- Connect the LineUP controller to the PC via USB
- Connect pressure pumps to the LineUP channels
- The SDK auto-detects via `fgt_detect()` — no manual configuration needed
- Up to 3 pressure channels are supported (2 main + 1 differential)

### Troubleshooting
| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `find_pumps()` returns 0 | USB not detected | Check USB cable, try different port |
| `fgt_init()` crashes | DLL not found | Ensure `fluigent-sdk` is installed in workspace |
| Channel reads -1 | Pump disconnected | Verify pump cable is secure |

## Basler Camera (a2A1920-160umBAS)

### Connection
- Connect via USB3 (USB-C) — the camera requires USB3 bandwidth
- Install Basler pypylon driver (bundled via `pypylon` pip package)
- The app filters by model name `a2A1920-160umBAS` — if using a different Basler model, update the check in `main.py`

### Bandwidth
The app sets bandwidth to 419 MB/s. If you encounter frame drops or "Bandwidth overflow" errors, reduce `target_fps` in the GUI or adjust bandwidth in `camera.py`.

## Arduino Stage (UNO R4 WiFi)

### Wiring
| Arduino Pin | Peripheral |
|-------------|------------|
| D3 | Stepper X-step |
| D4 | Stepper X-direction |
| D5 | Stepper Y-step |
| D6 | Stepper Y-direction |
| D7 | Stepper Z-step |
| D8 | Stepper Z-direction |
| Serial (COM) | USB to PC |

### Firmware
Flash `Arduino/maldi.ino` using the Arduino IDE. The board auto-detects as "uno wifi r4 cmsis-dap" (VID 9025, PID 4098).

### Troubleshooting
- If not detected, check the port number in Device Manager
- The app scans all serial ports and matches by VID/PID
- Serial baud rate: 115200