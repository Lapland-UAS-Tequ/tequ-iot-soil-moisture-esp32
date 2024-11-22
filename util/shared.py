from util.logging import Log
log = Log()

from util.config import Config
cfg = Config()

from util.esp32tools import ESP32Tools
e32 = ESP32Tools()

from util.wioe5 import WIOE5
e5 = WIOE5()

from ble.blescanner import BLEScanner
bt = BLEScanner()

from util.rs485soil import RS485Soil
mb = RS485Soil()