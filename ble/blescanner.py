import bluetooth
import struct
import utime
from util.shared import log
from util.shared import cfg
from util.shared import e32
from ble.decoder import decode_data

class BLEScanner:
    def __init__(self):
        self.ble = bluetooth.BLE()
        self.ble.irq(self.handle_irq)
        self.results = {}
        self.payload = []
        self.scanner = None
        
    def handle_irq(self, event, data):
        if event == 5:  # Event value for _IRQ_SCAN_RESULT           
            addr_type, addr, adv_type, rssi, adv_data = data           
            macAddr = bytes(addr).hex()

            if macAddr in cfg.TAGS:
                #print("RUUVITAG FOUND!")
                payload = bytes(adv_data)
                dataFormat = adv_data[7]
                if not macAddr in self.results:
                    ruuviTagData = decode_data(dataFormat, payload[5:])
                    self.results[macAddr] = {
                        "temperature": ruuviTagData[2],
                        "humidity": ruuviTagData[1],
                        "battery_voltage": ruuviTagData[7] / 1000
                    }
    def enable_ble(self):
        if not self.ble.active():
            self.ble.active(True)
            log.info("BLEScanner.enable_ble: Started Bluetooth with address of: %s" % self.ble.config("mac")[1].hex())
        else:
            log.info("BLEScanner.enable_ble: BLE already enabled.")
    
    def disable_ble(self):
        if self.ble.active():
            self.ble.active(False)
            log.info("BLEScanner.disable_ble: BLE disabled")
        else:
            log.info("BLEScanner.disable_ble: BLE already disabled.")
        
    def stop_scanning(self):
        try:
            if self.scanner is not None:
                self.scanner.stop()
        except Exception as e:
            log.error("BLEScanner.stop_scanning: Failed to stop scanning",e)
        else:
            log.info("BLEScanner.stop_scanning: BLE Scanning stopped.")
            
    def stop_scan(self):
        self.ble.gap_scan(None)
        return self.results

    def ble_scan(self):
        try:
            self.enable_ble()
            self.results = {}
            log.info("BLEScanner.ble_scan: Scanning for BLE advertisers for %.2f seconds..." % (cfg.BLE_TO/1000))
            self.scanner = self.ble.gap_scan(cfg.BLE_TO, cfg.BLE_IUS, cfg.BLE_WUS)
            utime.sleep(int(cfg.BLE_TO/1000))    
            self.stop_scanning()
        finally:
            self.disable_ble()
            return self.results        
    
