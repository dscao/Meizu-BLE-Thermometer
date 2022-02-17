# Meizu-BLE-Thermometer

ESPHome文件夹是给ESP32+ESPHome使用的，可以把ESP32作为一个蓝牙网关（GATT Client），序列执行读取蓝牙设备，目前做了小米两代蓝牙温度计和魅族蓝牙温度计支持。
使用方法：
1、使用pip安装的esphome:
将ESPHome文件夹内容放到Python的library文件夹的/site-packages/esphome/components/下，在ESPHome配置文件里加入配置，例子在example.yaml里。（可以使用命令： find / -name esp32_ble_tracker 查找文件夹）

2、使用hassio的addon安装的esphome：
放到 config/esphome/my_components 目录中

captive_portal:
external_components:
  - source: my_components
    components: [ esp32_ble_client, meizu_ble, meizu_ble_transmitter ]      
esp32_ble_client:
sensor:   
    - platform: meizu_ble
    update_interval: 300s
    mac_address: 68:3E:34:CC:E2:4D
    temperature:
      name: "Meizu Temperature Keting"
    humidity:
      name: "Meizu Humidity Keting"
    battery_level:
      name: "Meizu Battery Keting"
switch:
  - platform: restart  #用于重启NodeMCU
    name: "meizu_esp32_restart"
    id: meizu_esp32_restart

  - platform: meizu_ble_transmitter
    mac_address: 68:3E:34:CC:E2:4D
    name: "TVON"
    id: tvon
    uid: "5d001cc5ab3ba8439b"
    data: "55005d200024000001e0c39518b5cede1c09ced81c58cae62638fbba306fe6fe31cfe6ed3439e2e33837f2ed2839feeb2c3ffeed2c39faf33027ea8d4059968b445f968d445992834857a39c6948bca95e7e8c9f5d48bbd21205f9a8c2"
  
  - platform: meizu_ble_transmitter
    mac_address: 68:3E:34:CC:E2:4D
    name: "TVOFF"
    id: tvoff
    uid: "5d001cc5ab3ba8439b"
    data: "55005d200024000001e0c39518b5cede1c09ced81c58cae62638fbba306fe6fe31cfe6ed3439e2e33837f2ed2839feeb2c3ffeed2c39faf33027ea8d4059968b445f968d445992834857a39c6948bca95e7e8c9f5d48bbd21205f9a8c2"

  - platform: template
    name: "客厅电视开关"
    optimistic: true
    turn_on_action:
      - switch.turn_on: tvon
    turn_off_action:
      - switch.turn_on: tvoff      
      

3、使用docker安装的，在docker的/usr/src/app/esphome/components/文件夹下。
原理与addon安装一样。

另外，由于工作原理原因，esp32_ble_client和esp32_ble_tracker是冲突的，不能同时使用。
