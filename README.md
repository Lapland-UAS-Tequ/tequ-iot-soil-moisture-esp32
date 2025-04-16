This repository is developed in Kuituhamppu käyttöön -project

https://lapinamk.fi/hanke/kuituhamppu-kayttoon/

------------------------------------------------------------------------------------

# tequ-iot-soil-moisture-esp32
Soil moisture measurement system. Collects data from Ruuvitag sensors and DFRobot soil moisture sensors. In this project system is used to measure biomass temperature and moisture from three different locations (bottom, middle and top). Biomass is located in compost unit. 

System can send data using BLE or Wi-Fi connection.

Javascript module to receive and forward BLE advertisement data is programmed for Shelly devices. Data is forwarded to local MQTT broker. Javascript module is ble-soilmoisture.js in repository files.

System is designed to 6-12 months without need to change batteries.

## Hardware
Hardware components are built on PCB designed for the project and PCB is placed in industrial IP68 rated enclosure. 

Enclosure model is Hammond 1555EF17GY. 

https://www.mouser.fi/datasheet/2/177/1555f-1389823.pdf


| Hardware               | Model         | Placement       | Link          |
| -------------          |:-------------:| :-------------: | :-------------:|
| Main board             | Seeed XIAO ESP32S3 |  Enclosure     | <a href="https://docs.sixfab.com/docs/sixfab-pico-lte-introduction">Link</a>|
| RS485 Module           | Grove - RS485     |  Enclosure  | <a href="https://wiki.seeedstudio.com/Grove-RS485">Link</a>|
| DC/DC module           | Adafruit 4654     |  Enclosure     | <a href="https://www.adafruit.com/product/4654">Link</a>|
| Battery pack           | 3.7 LiPo 2000 mAh        | Enclosure   | <a href="https://www.suomenakut.fi/akut-ja-paristot/li-polymer-akku-3-7v-2000mah-lp674261-cl-mitat61mm-x-42mm-x-6-1mm/p/100263116540011">Link</a>|
| Soil moisture sensor   | DFRobot       | Composter | <a href="https://wiki.dfrobot.com/RS485_Soil_Sensor_Temperature_Humidity_SKU_SEN0600">Link</a>|


## Schematic

![Soil moisture system schematics](/schematics.png)




## Development

1. Install Thonny (https://thonny.org/)

3. Connect and verify ESP32
   
4. Build connections between devices and configure soil moisture sensors (Modbus addresses 11,12,13)
  
5. Update ESP32 Micropython using Thonny

6. Clone this repository
7. 
You can clone the repository with the command:
```
git clone https://github.com/Lapland-UAS-Tequ/tequ-iot-soil-moisture-esp32
```
or by downloading and unzipping the repository.

7. Create settings.json
   
In the repository you'll find template files. 

8 Open folder in Thonny and upload files into device
 
9. Run project and verify operation
