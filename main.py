from util.shared import log
from util.shared import cfg
from util.shared import e32
from util.shared import e5
from util.shared import bt
from util.shared import mb
from machine import deepsleep
from sys import print_exception
import utime
start = utime.ticks_ms()
import ujson
import gc
gc.enable()
e32.start_counter(3)

if cfg.WDT_ON:
    log.info("Boot - WDT enabled. WDT_TIMEOUT: %d seconds" % (cfg.WDT_TO/1000))
    from machine import WDT
    wdt = WDT(timeout=cfg.WDT_TO)

log.info("Boot - Program starting after %s" % e32.check_reset_cause())

try:
    log.info("Main - Soil moisture app version [2024-11-25] starting...")
    e32.blink_user_led(0.050,1)
    
    results = bt.ble_scan()
    print(results)
    
    log.info("Main - Turn on RS485 sensors...")
    e32.pwr_control(1)
    utime.sleep(1)
    data = mb.read_all_sensors()
    log.info(data)

    if cfg.E5_LOWPOWER:
        log.info("Main - WIO E5 module Auto low power is enabled.")
    else:
        log.info("Main - WIO E5 module enabling auto low power mode...")  
        e5.set_auto_lowpower()
        cfg.E5_LOWPOWER = 1
        cfg.update_config_file()
        utime.sleep(2)
    
    e5.disable_auto_lowpower()
    e5.normal_wake_up()    
    e5.get_dev_eui() 

    if cfg.E5_CONFIGURED:
        log.info("Main - WIO E5 module is configured")  
    else:
        log.info("Main - Configuring WIO E5 module...")
        e5.configure()
        cfg.E5_CONFIGURED = 1
        cfg.update_config_file()
       
    while 1:   
        joined = e5.join()        
        if joined:
            break
       
    if joined:
        log.info("Joining to LoRaWAN network...OK")
        dp_id = e32.packId(9)
        import random
        out_t = e32.packTemperature(random.randrange(-40,80))
        out_rh = e32.packHumidity(random.randrange(0,100))
        out_bat = e32.packBatteryVoltage(random.randrange(2000,3500))
        in_t = e32.packTemperature(random.randrange(-40,80))
        in_rh = e32.packHumidity(random.randrange(0,100))
        in_bat = e32.packBatteryVoltage(random.randrange(2000,3500))
        soil_t1 = e32.packTemperature(random.randrange(-40,80))
        soil_rh1 = e32.packHumidity(random.randrange(0,100))
        soil_t2 = e32.packTemperature(random.randrange(-40,80))
        soil_rh2 = e32.packHumidity(random.randrange(0,100))
        soil_t3 = e32.packTemperature(random.randrange(-40,80))
        soil_rh3 =  e32.packHumidity(random.randrange(0,100))
        
        payload_bytes = dp_id+out_t+out_rh+out_bat+in_t+in_rh+in_bat+soil_t1+soil_rh1+soil_t2+soil_rh2+soil_t3+soil_rh3
        payload_hex = payload_bytes.hex()
        
        resp = e5.send_data(payload_hex)
        if resp:
            log.info("Sending data...OK")
        else:
            log.info("Sending data...FAILED")
    else:
        log.info("Joining to LoRaWAN network...FAILED")     

    end = utime.ticks_ms()
    diff = utime.ticks_diff(end, start) / 1000
    log.info("Executing program took %.3f s" % diff)
except Exception as e:
    log.error("Main - Exception",e)
    e32.blink_user_led(0.100,1)
    utime.sleep(5)
finally:
    wdt.feed()
    e32.blink_user_led(0.050,5)
    e32.pwr_control(0)
    e5.set_auto_lowpower()
    utime.sleep(5)
    log.info("Go to deepsleep for %d seconds..." % cfg.SLEEPTIME)
    deepsleep(cfg.SLEEPTIME )