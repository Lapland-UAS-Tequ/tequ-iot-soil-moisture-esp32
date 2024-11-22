from sys import print_exception
from time import localtime

class Log:
    def __init__(self):
        self.LOGGING_ON = 1
      
    def print_info(self,string):
        logTime = localtime()
        logTime = "%02d-%02d-%02d %02d:%02d:%02d" % (
                logTime[0], logTime[1], logTime[2], logTime[3], logTime[4], logTime[5]
        )
        print("%s : %s" % (logTime, string))    
   
    def info(self, string):       
        if self.LOGGING_ON:        
            self.print_info(string)

    def set_logging(self,value):
        self.LOGGING_ON = value
        
        if value == 1:
            self.print_info("Log.set_logging: Logging is enabled.")
        else:
            self.print_info("Log.set_logging: Logging is disabled.")   
                
         

    def error(self, string, e):
        self.print_info(string)
        print_exception(e)