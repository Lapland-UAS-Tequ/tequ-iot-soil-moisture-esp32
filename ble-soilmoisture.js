let CONFIG = {
  mqtt_topic: "soil"
};

const SCAN_PARAM_WANT = { duration_ms: BLE.Scanner.INFINITE_SCAN, active: false};

let MFD_ID = "02e5";

function d2h(d) {
    var s = (d).toString(16);
    if(s.length < 2) {
        s = '0' + s;
    }
    return s;
}


function a2hex(str) {
  var arr = [];
  for (var i = 0, l = str.length; i < l; i ++) {
    var hex = Number(str.charCodeAt(i)).toString(16);    
    arr.push(d2h(hex));
  }
  return arr.join('');
}


function parseData(res) {
    try{
      let rm = {}
      addr = res.addr;
      addr  = addr.replace(":",""); 
      addr  = addr.replace(":","");
      addr  = addr.replace(":","");
      addr  = addr.replace(":","");
      addr  = addr.replace(":","");
      rm.addr = addr 
      rm.rssi = res.rssi;
      advData = res.advData
      rm.data = a2hex(advData)
      return rm;
    }
    catch(e){
      return null;
    }   
}

function publishToMqtt(measurement) {
  MQTT.publish(
    CONFIG.mqtt_topic + "/" + measurement.addr,
    JSON.stringify(measurement)
  );
}

function scanCB(ev, res) {
  if (ev !== BLE.Scanner.SCAN_RESULT) return;
   if(res.manufacturer_data){
    mfd_data = res.manufacturer_data
    id = Object.keys(mfd_data)[0]
    //print(id)    
    if(id == MFD_ID ){
      let measurement = parseData(res);  
       if (measurement === null) return;
       print("ble-soilmoisture | new measurement:", JSON.stringify(measurement));
       publishToMqtt(measurement);
    }
    else{
      return;
    } 
  }
}

function init(){
  print("Starting ble-soilmoisture.js script...");
  // get the config of ble component
  const BLEConfig = Shelly.getComponentConfig("ble");

  // exit if the BLE isn't enabled
  if (!BLEConfig.enable) {
    print("ble-soilmoisture | Error: The Bluetooth is not enabled, please enable it from settings");
    return;
  }

  // check if the scanner is already running
  if (BLE.Scanner.isRunning()) {
    print("ble-soilmoisture | Info: The BLE gateway is running, the BLE scan configuration is managed by the device");
  }
  else {
    // start the scanner
    print("ble-soilmoisture | Starting new BLE scanner...");
    const bleScanner = BLE.Scanner.Start(SCAN_PARAM_WANT);

    if (!bleScanner) {
      print("ble-soilmoisture | Error: Can not start new scanner");
    }
  }

  // subscribe a callback to BLE scanner
  BLE.Scanner.Subscribe(scanCB);
}

init();
