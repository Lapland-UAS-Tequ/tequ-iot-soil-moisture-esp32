from util.shared import log
from util.shared import cfg
from machine import UART
from machine import Pin
import utime
from uModBus.serial import Serial
import struct

class RS485Soil:
    def __init__(self):      
       self.mb = Serial(uart_id=2, baudrate=9600, data_bits=8, stop_bits=1, parity=None, tx=Pin(3), rx=Pin(4))
       self.sensors = cfg.SENSORS
             
    def read_single_sensor_data(self, sensor_id):
        try:
            log.info("RS485Soil.read_single_sensor_data: MB_ID: %d" % sensor_id)
            registers = bytes(self.mb.read_holding_registers(sensor_id, 0x0, 2, True))        
            h = struct.unpack(">H", registers[0:2])[0] * 0.1
            t = struct.unpack(">H", registers[2:4])[0] * 0.1
            return {"sid":sensor_id,"data":{"h":h,"t":t}}
        except Exception as e:
            log.error("RS485Soil.read_single_sensor_data",e)
            return {"sid":sensor_id,"data":{"h":None,"t":None}}
       
    def read_all_sensors(self):
        data = {}
        for sensor_id in self.sensors:
            single_data = self.read_single_sensor_data(sensor_id)
            sid = single_data["sid"]
            d = single_data["data"]
            data[sid] = d        
        return data
    