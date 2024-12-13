from util.shared import log
from util.shared import cfg
from machine import UART
from machine import Pin
import utime
from util.shared import e32

class WIOE5:
    def __init__(self):
        self.uart = UART(1,baudrate=9600, parity=None, bits=8, stop=1, tx=Pin(1), rx=Pin(2), timeout=1000)
        
    def send_command(self, command):
        log.info("WIOE5.send_command: Sending command: %s" % command)
        self.uart.write(command+"\r")
            
    def read_uart(self):
        line = self.uart.readline()
        response = ""
        try:
            response = line.decode()
            #log.info("WIOE5.read_uart: AT RESPONSE: "+response)
        except:
            pass       
        return response


    def command_routine(self,command,ok_responses):     
        ok = False
        count = 0  
        self.send_command(command)
        
        while not ok:   
            response = self.read_uart()                
            for ok_resp in ok_responses:
                if ok_resp in response:        
                    log.info("WIOE5.command_routine: "+response)
                    if len(ok_responses) == 1:
                        return True
                    else:
                        return {"response": response, "status":True}
            count = count + 1
            utime.sleep(0.250)
            if count > 5:
                return False

    def set_lwotaa_mode(self):
        return self.command_routine("AT+MODE=LWOTAA",["+MODE: LWOTAA"])    

    def set_app_key(self):
        return self.command_routine('AT+KEY=APPKEY,"'+cfg.APPKEY+'"',["+KEY: APPKEY "+cfg.APPKEY])
      
    def set_app_eui(self):
        return self.command_routine('AT+ID=AppEui,"'+cfg.APPEUI+'"',["+ID: AppEui,"])    
      
    def get_dev_eui(self):
        return self.command_routine("AT+ID=DevEui",["+ID: DevEui,"])    
     
    def configure(self):
        r1 = self.set_app_eui()
        r2 = self.set_app_key()
        r3 = self.set_lwotaa_mode()

    def join(self):        
        joined = False  
        resp = self.command_routine("AT+JOIN",["+JOIN: Start","+JOIN: Joined already"])
        
        if "+JOIN: Joined already" in resp["response"]:
            joined = True
        else:
            joined = False    
        
        if joined:
            return joined
        
        while not joined:
            response = self.read_uart()
            
            if "+JOIN: NORMAL" in response:
                log.info("WIOE5.join.normal:"+response)
                
            elif "+JOIN: NetID" in response:
                log.info("WIOE5.join.NetID: "+response)    
                
            elif "+JOIN: Joined already" in response:
                log.info("WIOE5.join.joined_already: "+response)
                return True
            elif "+JOIN: Join failed" in response:
                log.info("WIOE5.join.failed: "+response)
                response = self.read_uart()
                log.info("WIOE5.join.failed: "+response)
                return False
            elif "+JOIN: Done" in response:
                log.info("WIOE5.join.done: "+response)
                return True 
            else:
                log.info("WIOE5.join: Trying to join...")       
                e32.blink_user_led(0.500,1)

    def send_data(self, data):
        self.send_command("AT+CMSGHEX="+data)
        data_sent = False   
           
        while not data_sent:
            response = self.read_uart()
            #blink_led(2)
            
            if "+CMSGHEX: Done" in response:
                log.info("WIOE5.send_data: Done")
                data_sent = True
                break 
            else:
                data_sent = False   
        return data_sent

    def normal_wake_up(self):
        return self.command_routine("AT\r",["+AT: OK"])
          
    def disable_auto_lowpower(self):
        return self.command_routine("\xff\xff\xff\xffAT+LOWPOWER=AUTOOFF\r",["+LOWPOWER: AUTOOFF"])
                
    def set_auto_lowpower(self):
        self.send_command("\xff\xff\xff\xffAT+LOWPOWER=AUTOON\r")
       