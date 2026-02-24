# fluigent dependencies
from Fluigent.SDK import fgt_detect, fgt_init, fgt_close
from Fluigent.SDK import fgt_get_controllersInfo
from Fluigent.SDK import fgt_get_pressureChannelCount, fgt_get_pressureChannelsInfo
from Fluigent.SDK import fgt_set_pressure, fgt_get_pressure, fgt_get_pressureRange

from functools import wraps

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
        self.detect()

    def detect(self):
        SNs, _ = fgt_detect()
        controllerCount = len(SNs)
        if controllerCount > 0:
            self.SN = SNs[0]
        else:   
            print("No controllers detected!")

    def check(self):
        if len(self.SN) > 0:
            return True
        print("No controller connected!")
        return False

    @check_connection
    def initialize(self):
        fgt_init(self.SN)

    @check_connection
    def set_pressure(self, pump_idx, pressure, stdout=True):
        fgt_set_pressure(pump_idx, pressure)
        pressureMeasurement = fgt_get_pressure(pump_idx)
        if stdout:
            l1, l2 = f"Setpoint", f"Current pressure:"
            output = (f"[{pump_idx:<1}] {l1:<18} {pressure:04d} mBar\n"
                      f"{'':<4} {l2:<18}{pressureMeasurement:.4f} mBar")
            print(output)

    @check_connection
    def get_pressure(self, pump_idx) -> float:
        return fgt_get_pressure(pump_idx)

    @check_connection
    def get_range(self, pump_idx) -> (float, float):
        minPressure, maxPressure = fgt_get_pressureRange(pump_idx)
        return (minPressure, maxPressure)

    @check_connection
    def reset_all(self):
        for pump_idx in range(fgt_get_pressureChannelCount()):
            fgt_set_pressure(pump_idx, 0)

    @check_connection
    def zero_pump(self, pump_idx):
        fgt_set_pressure(pump_idx, 0)

    @check_connection
    def calibrate_pump(self, pump_idx):
        fgt_calibratePressure(pump_idx)

    @check_connection
    def close(self):
        fgt_close()