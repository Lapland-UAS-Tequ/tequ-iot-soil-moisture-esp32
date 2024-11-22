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
            rh_b = registers[0:1]
            rh = struct.unpack(">H", registers[0:1])[0] * 0.1
            t_b = registers[1:2]
            t = struct.unpack(">H", registers[1:2])[0] * 0.1
            return {"sid":sensor_id,"data":{"rh":rh,"t":t, "rh_b":rh_b,"t_B":t_b}}
        except Exception as e:
            log.error("RS485Soil.read_single_sensor_data",e)
            return {"sid":sensor_id,"data":{"rh":None,"t":None, "rh_b":None,"t_b":None}}
       
    def read_all_sensors(self):
        data = {}
        for sensor_id in self.sensors:
            single_data = self.read_single_sensor_data(sensor_id)
            sid = single_data["sid"]
            d = single_data["data"]
            data[sid] = d        
        return data
    