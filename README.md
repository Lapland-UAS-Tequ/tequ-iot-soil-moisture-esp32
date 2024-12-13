This repository is developed in Kuituhamppu käyttöön -project

https://lapinamk.fi/hanke/kuituhamppu-kayttoon/

------------------------------------------------------------------------------------

# tequ-iot-soil-moisture-esp32
Soil moisture measurement system. Collects data from Ruuvitag sensors and DFRobot soil moisture sensors. In this project system is used to measure biomass temperature and moisture from three different locations (bottom, middle and top). Biomass is located in compost unit. Ruuvitag sensors are used to measure outdoor and indoor temperature and relative humidity.

System can send data to cloud using wifi connection or LoRaWAN.

System is designed to work multiple years without need to change batteries.

## Hardware
Hardware components are placed industrial IP68 rated enclosure. 

| Hardware               | Model         | Placement       | Link          |
| -------------          |:-------------:| :-------------: | :-------------:|
| Main board             | Seeed XIAO ESP32S3|  Enclosure     | <a href="https://docs.sixfab.com/docs/sixfab-pico-lte-introduction">Link</a>|
| LoRaWAN module*        | Grove Wio-E5      |     | <a href="https://wiki.seeedstudio.com/Grove_LoRa_E5_New_Version">Link</a>|
| RS485 Module           | Grove - RS485     |    | <a href="https://wiki.seeedstudio.com/Grove-RS485">Link</a>|
| DC/DC module           | Adafruit       |       | <a href="">Link</a>|
| Battery pack           | 3x1.5 AA          |    | <a href="">Link</a>|
| Outdoor sensor         |         |    | <a href="">Link</a>|
| Indoor sensor          |         |    | <a href="">Link</a>|
| Soil moisture sensor   |         |    | <a href="">Link</a>|

* LoRAWAN module is optional.

## Connections
Connections of the hardware used in prototype.

| Device                 | PIN           | Device         | PIN            | 
| -------------          |:-------------:| :-------------:| :-------------:|
| Main board             | BAT+          | Battery pack   | Battery +      |
| Main board             | BAT-          | Battery pack   | Battery -      |
| DC/DC module           | VIN           | Battery pack   | Battery +      |
| DC/DC module           | GND           | Battery pack   | Battery - (GND)|
| DC/DC module           | EN            | Main board     | GPIO9 (D10)    |
| LoRaWAN module         | GND           | Battery pack   | GND            |
| LoRaWAN module         | VCC           | Main board     | 3V3            |
| LoRaWAN module         | UART TX       | Main board     | GPIO1 (D0)     |
| LoRaWAN module         | UART RX       | Main board     | GPIO2 (D1)     |
| RS485 module           | GND           | Battery pack   | GND            |
| RS485 module           | VCC           | DC/DC module   | 5V             |
| RS485 module           | UART TX       | Main board     | GPIO3 (D2)     |
| RS485 module           | UART RX       | Main board     | GPIO4 (D3)     |
| Soil sensor 1,2,3      | GND           | Battery pack   | GND            |
| Soil sensor 1,2,3      | VIN           | DC/DC module   | 5V             |
| Soil sensor 1,2,3      | GND           | RS485 modul    | RS485 TX       |
| Soil sensor 1,2,3      | GND           | RS485 modul    | RS485 RX       |


Connection diagram:

***TBD***

## Development

1. Install Thonny (https://thonny.org/)

3. Connect and verify ESP32
   
4. Build connections between devices
   
5. Add LoRaWAN module to Digita LoRaWAN portal (or any other compatible platform you like to use)

6. Update ESP32 Micropython using Thonny

7. Clone this repository
You can clone the repository with the command:
```
git clone https://github.com/Lapland-UAS-Tequ/tequ-iot-soil-moisture-esp32
```
or by downloading and unzipping the repository.

8. Create settings.json
In the repository you'll find template files. 

9. Open folder in Thonny and upload files into device
 
10. Run project and verify operation
