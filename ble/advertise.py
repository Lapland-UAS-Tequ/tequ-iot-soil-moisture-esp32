import bluetooth
import struct
import utime
from util.shared import log
from util.shared import cfg
from util.shared import e32
from machine import unique_id

def form_adv_name(name):
    payload = bytearray()
    payload.append(len(name) + 1)
    payload.append(0x09)
    payload.extend(name.encode())
    return payload

def form_adv_data_dp1(name, data):
    payload = bytearray()
    custom_data = bytearray(data)
    
    payload.append(0x02)
    payload.append(0x01)
    payload.append(0x06)
    
    payload.append(len(name) + 1)
    payload.append(0x09)
    payload.extend(name.encode())
          
    payload.append(len(custom_data) + 4)   # datapacket length
    payload.append(0xFF)            # 0xFF
    payload.append(0xE5)            # Manufacturer specific
    payload.append(0x02)            # Manufacturer specific
    payload.append(0x01)            # Datapacket ID
    payload.extend(custom_data)     # CUSTOM DATA
    return payload

class BLEAdvertise:
    def __init__(self):
        log.info("BLEAdvertise.Configuring BLE...")
        self.ble = bluetooth.BLE()
        
        
    def advertise(self, advertise_interval_us, name, data, datapacket_id):
         # log("Started Bluetooth with address of: {}".format(form_mac_address(ble.config("mac"))))
        #name = unique_id()
        #name = name.hex()
        payload = form_adv_data_dp1(name, data)
        log.info("BLEAdvertise.advertise: Payload size %d bytes" % len(payload))
        log.info("BLEAdvertise.advertise: Advertising payload: {}".format(payload))
        self.ble.gap_advertise(advertise_interval_us, payload)

    def enable_ble(self):
        if not self.ble.active():
            self.ble.active(True)
            log.info("BLEAdvertise.enable_ble: Started Bluetooth with address of: %s" % self.ble.config("mac")[1].hex())
        else:
            log.info("BLEAdvertise.enable_ble: BLE already enabled.")
    
    def disable_ble(self):
        if self.ble.active():
            self.ble.active(False)
            log.info("BLEAdvertise.disable_ble: BLE disabled")
        else:
            log.info("BLEAdvertise.disable_ble: BLE already disabled.")

    def stopAdvertise(self):
        self.ble.gap_advertise(None)

    def advertiseOnce(self, sleep_time_ms, advertise_interval_us, name, data, datapacket_id):
        try:
            self.enable_ble()
            self.advertise(advertise_interval_us, name, data, datapacket_id)
            utime.sleep_ms(sleep_time_ms)
            self.stopAdvertise()
        except Exception as e:
            log.error("BLEAdvertise.advertise: - Exception",e)    
        finally:
            self.stopAdvertise()
            self.disable_ble()