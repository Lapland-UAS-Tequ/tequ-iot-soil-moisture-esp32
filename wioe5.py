from tools.shared import log
from tools.shared import cfg

class WIOE5:
    def __init__(self):
        self.uart = UART(1,baudrate=9600, parity=None, bits=8, stop=1, tx=Pin(1), rx=Pin(2), timeout=1000)
        
    def send_command(self, command):
        log.info("Sending command: %s" % command)
        self.uart.write(command+"\r")
        
    def read_uart(self):
        line = self.uart.readline()
        response = ""
        try:
            response = line.decode()
            log.info("AT RESPONSE: "+response)
        except:
            pass       
        return response

    def set_app_key(self):
        self.send_command("AT+KEY="+cfg.APPKEY)
        key_set = False
        
        while not key_set:
            response = self.read_uart()           
            if "+KEY: APPKEY "+key in response:
                log.info("APPKEY set")
                break 
            else:
                key_set = False
        return key_set
    
    def set_app_eui(self):
        self.send_command('AT+ID=AppEui,"'+cfg.APPEUI+'"')
        app_eui_set = False
        
        while not app_eui_set:
            response = self.read_uart()           
            if "+ID: AppEui," in response:
                log.info("APPEUI set")
                app_eui_set = True
                break 
            else:
                app_eui_set = False
         return app_eui_set
        

    def wioe5_join(self):        
        self.send_command("AT+JOIN")
        joined = False   
           
        while not joined:
            response = self.read_uart()
            #blink_led(1)
            
            if "+JOIN: Start" in response:
                log.info("wioe5_join: Join process started")
            elif "+JOIN: NORMAL" in response:
                log.info("wioe5_join: Normal join process")
            elif "+JOIN: Joined already" in response:
                log.info("wioe5_join: Already joined")
                joined = True
                break
            elif "+JOIN: Join failed" in response:
                log.info("wioe5_join: Failed")
                joined = False
                break
            elif "+JOIN: Done" in response:
                log.info("wioe5_join: Done")
                joined = True 
                break 
            else:
                log.info("wioe5_join: Trying to join...")       
        return joined


    def wioe5_send_data(self, data):
        self.send_command("AT+CMSGHEX="+data)
        data_sent = False   
           
        while not data_sent:
            response = self.read_uart()
            #blink_led(2)
            
            if "+CMSGHEX: Done" in response:
                log.info("send_data: Done")
                data_sent = True
                break 
            else:
                data_sent = False   
        return data_sent

    def wioe5_normal_wake_up(self):
        log.info("WIOE5.wioe5_wake_up")       
        self.send_command("AT\r")
        waked_up = False
        
        while not waked_up:
            response = self.read_uart()
            #blink_led(1)
            
            if "+LOWPOWER: AUTOOFF" in response:
                log.info("wake_up: Device online")
                waked_up = True
                break
            else:
                waked_up = False    
        return waked_up




    def wioe5_wake_up(self):
        log.info("WIOE5.wioe5_wake_up")       
        self.send_command("\xff\xff\xff\xffAT+LOWPOWER=AUTOOFF\r")
        waked_up = False
        
        while not waked_up:
            response = self.read_uart()
            #blink_led(1)
            
            if "+LOWPOWER: AUTOOFF" in response:
                log.info("wake_up: Device online")
                waked_up = True
                break
            else:
                waked_up = False    
        return waked_up
        
    def wioe5_set_lowpower(self):
        log.info("Send AT+LOWPOWER=AUTOON\r...")
        self.send_command("\xff\xff\xff\xffAT+LOWPOWER=AUTOON\r")  
        return True
