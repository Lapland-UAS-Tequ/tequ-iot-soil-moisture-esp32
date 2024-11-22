import time
import ujson
from util.shared import log

class Config:
    def __init__(self):
        self.configuration = {}
        self.CONFIG_FILE = "settings.json"
        
        # Default values
        self.SLEEPTIME = 3600
        self.DATA_PATH = ""
        self.BLE_TO = 5500
        self.BLE_IUS = 50000
        self.BLE_WUS = 50000
        self.DEBUG_LVL = 3
        self.WDT_ON = 0
        self.WDT_TO = 90
        self.LOG_ON = 1
        self.TAGS = []
        self.APPEUI = ""
        self.APPKEY = ""
        self.APPKEY_SET = 0
        self.APPEUI_SET = 0
        self.E5_LOWPOWER = 0
        self.E5_CONFIGURED = 0
        self.SENSORS = [1,2,3]
        
        
        # Read values from config-file
        self.read_config()
        
    def read_config(self):
        try:
            file = open(self.CONFIG_FILE)
            settings = ujson.loads(file.read())
            
            self.configuration = settings
            self.SLEEPTIME = settings['SLEEPTIME']
            self.BLE_TO = settings['BLE_TO']
            self.BLE_IUS = settings['BLE_IUS']
            self.BLE_WUS = settings['BLE_WUS']
            self.WDT_TO = settings["WDT_TO"]
            self.WDT_ON = settings["WDT_ON"]
            self.LOG_ON = settings["LOG_ON"]
            self.TAGS = settings["TAGS"]
            self.APPEUI = settings["APPEUI"]
            self.APPKEY = settings["APPKEY"]
            self.APPKEY_SET = settings["APPKEY_SET"]
            self.APPEUI_SET = settings["APPEUI_SET"]
            self.E5_LOWPOWER = settings["E5_LOWPOWER"]
            self.E5_CONFIGURED = settings["E5_CONFIGURED"]
            self.SENSORS = settings["SENSORS"]
       
            log.info("Config.read_config: Opening configuration file... OK")
            log.info("Config.read_config: Configuration: %s" % str(self.configuration))
        except Exception as e:
            log.error("Config.read_config: Reading configuration file... FAILED",e)         
        finally:
            file.close()    

    def update_config_file(self):
        config_update_ok = False
        try:
            log.info("Config.update_config_file: Updating config file...")
            file = open(self.CONFIG_FILE, mode='w')
            
            settings = {}
            settings['SLEEPTIME'] = self.SLEEPTIME
            settings['BLE_TO'] = self.BLE_TO
            settings['BLE_IUS'] = self.BLE_IUS
            settings['BLE_WUS'] = self.BLE_WUS          
            settings["WDT_TO"] = self.WDT_TO
            settings["WDT_ON"] = self.WDT_ON
            settings["LOG_ON"] = self.LOG_ON
            settings["TAGS"] = self.TAGS
            settings["APPEUI"] = self.APPEUI
            settings["APPKEY"] = self.APPKEY
            settings["APPEUI_SET"] = self.APPEUI_SET
            settings["APPKEY_SET"] = self.APPKEY_SET
            settings["E5_LOWPOWER"] = self.E5_LOWPOWER
            settings["E5_CONFIGURED"] = self.E5_CONFIGURED
            settings["SENSORS"] = self.SENSORS
                        
            file.write(ujson.dumps(settings))         
            log.info("Config.update_config_file: Updating config file...OK")
            config_update_ok = True
        except:
            log.error("Config.update_config_file: Updating config file...FAILED")              
        finally:
            file.close()
        
        return config_update_ok
            
    def update_config_value(self, param, value): 
        if hasattr(self,param):  
            if getattr(self,param) != value:
                valid_value = self.check_parameter_validity(param,value)
                setattr(self,param,valid_value)
                log.info("Config.update_config_value: New value %s=%s" % (param,valid_value))               
                return True
            else:
                log.info("Config.update_config_value: Parameter value has not changed.")
                return False
        else:
            log.info("Config.update_config_value: No parameter %s" % param)
            return False
    
    def check_parameter_validity(self,parameter,value):
        limits = {            
            "BLE_TO":{"type":"int","low":1000,"high":15000},
            "BLE_IUS":{"type":"int","low":10000,"high":100000},
            "BLE_WUS":{"type":"int","low":10000,"high":100000},
            "SLEEPTIME":{"type":"int","low":5,"high":604800},
            "WDT_ON":{"type":"enum","allowed":[0,1],"default":1},
            "WDT_TO":{"type":"int","low":30,"high":300}, 
            "TAGS":{"type":"text"},
            "APPEUI":{"type":"text"},
            "APPKEY":{"type":"text"},
            "APPEUI_SET":{"type":"enum","allowed":[0,1],"default":0},
            "APPKEY_SET":{"type":"enum","allowed":[0,1],"default":0},
            "E5_LOWPOWER":{"type":"enum","allowed":[0,1],"default":0},
            "E5_CONFIGURED":{"type":"enum","allowed":[0,1],"default":0},
            "SENSORS":{"type":"text"}
        }
        
        parameter_limits = limits[parameter]
        parameter_value = value
        param_type = parameter_limits["type"]

        if param_type == "text":
            pass
        elif param_type == "url":
            pass
        elif param_type == "email":
            pass
        elif param_type == "enum":
            allowed_values = parameter_limits["allowed"]
            default_value = parameter_limits["default"]
            if parameter_value in allowed_values:
                return parameter_value
            else:
                log.info("Config.check_parameter_validity. Value %d not allowed. Return default value." % parameter_value)  
                return default_value
        elif param_type == "int":
            low = parameter_limits["low"]    
            high = parameter_limits["high"]
            
            if parameter_value < low:  
                log.info("Config.check_parameter_validity. %d < %d. Return default LOW." % (parameter_value,low))  
                return low  
            elif parameter_value > high:
                log.info("Config.check_parameter_validity. %d > %d. Return default HIGH." % (parameter_value,high)) 
                return high
            else:
                return parameter_value

    def check_parameters(self, config_data):           
        changes = "\r\n"
        config_changed = False
        for parameter in config_data:
            value = config_data[parameter]
            log.info("Config.check_parameters: Parameter: %s Value: %s" % (parameter, value))
            parameter_changed = self.update_config_value(parameter.upper(),config_data[parameter])
            if parameter_changed:
                config_changed = True
                changes = changes + "%s => %s\r\n" % (parameter, getattr(self,parameter))
                
        result = {"changed":config_changed,"changes":changes}       
        return result 