# Weather-Station-with-ESP8266-and-Homesassistant
Weather Station wilt ESP8266-12E and Oled Display SSD1306 

**Framework used: Arduino**

**IDE used**:
[PlatformIO Core](http://platformio.org/get-started/cli)

**MQTT publisher: Home Assistant Hass)**
[HomeAssistant](https://home-assistant.io/)

HomeAssistant publishes data through MQTT on topic "sensor/#"

Here my configuration.yaml for the MQTT part:

```bash
- alias: 'mqttpublish temp_int'                                                      
  trigger:                                                                           
   platform: time                                                                    
   # You can also match on interval. This will match every 5 minutes                 
   minutes: '/5'                                                                     
   seconds: '00'                                                                     
  action:                                                                            
   service: mqtt.publish                                                             
   data:                                                                             
    topic: "sensor/temp_int"                                                         
    payload_template: "{{ states('sensor.interieur_temperature') }}"                 
- alias: 'mqttpublish temp_ext'                                                      
  trigger:                                                                           
   platform: time                                                                    
   # You can also match on interval. This will match every 5 minutes                 
   minutes: '/5'                                                                     
   seconds: '00'                                                                     
  action:                                                                            
   service: mqtt.publish                                                             
   data:                                                                             
    topic: "sensor/temp"                                                             
    payload_template: "{{ states('sensor.ext_sensor_temperature') }}"                
                                                                                     
- alias: 'mqttpublish icone'                                                         
  trigger:                                                                           
   platform: time                                                                    
   # You can also match on interval. This will match every 5 minutes                 
   minutes: '/5'                                                                     
   seconds: '00'                                                                     
  action:                                                                            
   service: mqtt.publish                                                             
   data:                                                                             
    topic: "sensor/icone"                                                            
    payload_template: "{{ states('sensor.weather_symbol') }}"                        
                                                                                     
- alias: 'mqttpublish danger'                                                        
  trigger:                                                                           
   platform: time                                                                    
   # You can also match on interval. This will match every 5 minutes                 
   minutes: '/5'                                                                     
   seconds: '00'                                                                     
  action:                                                                            
   service: mqtt.publish                                                             
   data:                                                                             
    topic: "sensor/danger"                                                           
    payload_template: "{{ states('sensor.pws_alerts') }}"

```

Weather symbols are provided by [yr](http://om.yr.no/symbol/)

More informations regarding implementation with Hass [here](https://home-assistant.io/components/sensor.yr/)

Danger symbol is provided by [wundergroud](https://www.wunderground.com/EU/FR/064.html)

More informations regarding implementation with Hass [here](https://home-assistant.io/components/sensor.wunderground/) 


![Alt text](./station.jpg)
