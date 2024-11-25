from machine import ADC
import machine
import utime
from util.shared import cfg
from util.shared import log
import esp32
import gc
from machine import reset_cause
from machine import Pin
from struct import pack,unpack

class ESP32Tools:
    def __init__(self):  
        self.user_led = machine.Pin(21,Pin.OUT)
        self.pwr_led = machine.Pin(9,Pin.OUT)
   
    def blink_user_led(self, interval, times):       
        initial_state = self.user_led()
        for x in range(times):
            self.user_led(1)
            utime.sleep(interval)
            self.user_led(0)
            utime.sleep(interval)
            self.user_led(1)
            utime.sleep(interval)
        self.user_led(initial_state) 
            
    def set_user_led_on(self): 
        self.user_led(1)
   
    def set_user_led_off(self): 
        self.user_led(0)
    
    def toggle_user_led(self): 
        self.user_led.toggle()
   
    def ReadTemperature(self):
        return esp32.mcu_temperature()
     
    def get_free_space(self):
        from os import statvfs
        stat = statvfs("/")
        KB = 1024
        MB = 1024 * 1024
        size = (stat[1] * stat[2]) / KB
        free = (stat[0] * stat[3]) / KB
        used = (size - free) / KB   
        result = {"free":free,"size":size,"used":used}   
        return result

    def get_memory(self):
        result = {"free":gc.mem_free(),"alloc":gc.mem_alloc()}   
        return result
    
    def check_reset_cause(self):
        reason = reset_cause()
        reset_txt = ""
       
        if reason == 1:
            reset_txt = "PWRON_RESET"
        elif reason == 2:
            reset_txt = "HARD_RESET"
        elif reason == 3:    
            reset_txt = "WDT_RESET"
        elif reason == 4:
            reset_txt = "DEEPSLEEP_RESET"
        elif reason == 5: 
            reset_txt = "SOFT_RESET"
        else:
            reset_txt = "UNKNOWN_RESET"
        
        return reset_txt

    def start_counter(self,seconds):
        count = seconds
        while count > 0:  
            log.info("Starting in %d seconds..." % count)
            count = count - 1
            utime.sleep(1)
            self.blink_user_led(0.050,1)

    def local_ts(self):
        ts = utime.localtime()
        return "%02d-%02d-%02d %02d:%02d:%02d" % (ts[0], ts[1], ts[2], ts[3], ts[4], ts[5])
          
    def pwr_control(self,value):
        self.pwr_led(value)           
        
    def packBatteryVoltage(self, value):
        #Map battery voltage 2000-3500 to range 0-255 with offset
        return pack("B",int((value-2000)/(1500/255)))
    
    def packTemperature(self, value):
        #Pack temperature to range -32768...+32767
        return pack("h",int(value*100))
    
    def packHumidity(self, value):
        #Map humidity 0-100 to range 0-255
        return pack("H",int(value*100))
    
    def packId(self,value):
        return pack("B",int(value))

    

