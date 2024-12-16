from util.shared import log
from util.shared import cfg
from util.shared import e32
from util.shared import bt
from util.shared import mb
from machine import deepsleep
from machine import unique_id
from sys import print_exception
import utime
start = utime.ticks_ms()
import ujson
import gc
gc.enable()

e32.user_led(1)
#e32.start_counter(3)

if cfg.LORAWAN:
    log.info("Main - LoRaWAN is enabled.")
    from util.shared import e5   

if cfg.WLAN:
    log.info("Main - WLAN is enabled.")
    import network
    import urequests as requests   

if cfg.WDT_ON:
    log.info("Boot - WDT enabled. WDT_TIMEOUT: %d seconds" % (cfg.WDT_TO/1000))
    from machine import WDT
    wdt = WDT(timeout=cfg.WDT_TO)

log.info("Boot - Program starting after %s" % e32.check_reset_cause())

try:
    log.info("Main - Soil moisture app version [2024-12-05] starting...")
    results = bt.ble_scan()
    print(results)
    if cfg.WLAN:
        wlan = network.WLAN(network.WLAN.IF_STA)
        wlan.active(True)
        wlan.connect(cfg.SSID, cfg.PW)
    log.info("Main - Turn on RS485 sensors...")
    e32.pwr_control(1)
    #utime.sleep(0.5)
    data = mb.read_all_sensors()
    log.info(data)
    e32.pwr_control(0)

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

    if cfg.WLAN:
        try:
            while not wlan.isconnected():
                log.info("Main - WLAN: Trying to connect...")       
                e32.blink_user_led(0.250,1)
            
            log.info("WLAN config: "+ str(wlan.ifconfig()))   
            user_headers = {
                 "content-type": 'application/json',
                 "x-meta-id":unique_id().hex(),
                 "x-meta-type":"esp32"
            }
            
            post_data = ujson.dumps({ "data": payload_hex})
            request_url = 'https://data.tequ.fi/' + 'api/soilmoisture'
            res = requests.post(request_url, headers=user_headers, data = post_data, timeout=5)
            
            if res.status_code == 200:
                e32.blink_user_led(0.020,10)
                log.info("Sending data...OK")
            else:
                log.info("Sending data...FAILED")
        except:
            log.error("Main - Wifi send - Exception",e)    
        finally:
            wlan.active(False)
        
    if cfg.LORAWAN:
        if cfg.E5_LOWPOWER:
            log.info("Main - WIO E5 module Auto low power is enabled.")
        else:
            log.info("Main - WIO E5 module enabling auto low power mode...")  
            e5.set_auto_lowpower()
            cfg.E5_LOWPOWER = 1
            cfg.update_config_file()
            utime.sleep(0.5)    
        e5.disable_auto_lowpower()
        e5.normal_wake_up()    
    
        if cfg.E5_CONFIGURED:
            log.info("Main - WIO E5 module is configured")  
        else:
            log.info("Main - Configuring WIO E5 module...")
            e5.configure()
            cfg.E5_CONFIGURED = 1
            cfg.update_config_file()
            e5.get_dev_eui() 
       
        while 1:   
            joined = e5.join()        
            if joined:
                break
       
        if joined:
            log.info("Joining to LoRaWAN network...OK")           
            resp = e5.send_data(payload_hex)
            if resp:
                e32.blink_user_led(0.050,10)
                log.info("Sending data...OK")
            else:
                log.info("Sending data...FAILED")
        else:
            log.info("Joining to LoRaWAN network...FAILED")
       
except Exception as e:
    log.error("Main - Exception",e)
    e32.blink_user_led(2,1)
    utime.sleep(3)
finally:
    wdt.feed()
    e32.pwr_control(0)
    if cfg.LORAWAN:
        e5.set_auto_lowpower()
    end = utime.ticks_ms()
    diff = utime.ticks_diff(end, start) / 1000
    log.info("Executing program took %.3f s" % diff)
    log.info("Go to deepsleep for %d seconds..." % int(cfg.SLEEPTIME/1000))
    deepsleep(cfg.SLEEPTIME)