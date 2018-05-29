#!/usr/bin/python

import time
import datetime
import paho.mqtt.client as paho
import threading

freq = 30 
start_time = 0

def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ESP/alive")

def offmessage():
    (rc, mid) = client.publish("ESP/alive", "OFF", qos=1)
    time.sleep(freq)

def on_message(client, userdata, msg):
    if "ON" in str(msg.payload):
     global start_time 
     start_time = time.time()

class MyThread(threading.Thread):
    def run(self):
	global start_time
 	while True:
   	 now = time.time()
	 time.sleep(freq)
         #If the Weather Station has not sent ON after 120s , then we publish OFF: This is handled by hass
   	 if (now - start_time) > 120:
           offmessage()

#MQTT
client = paho.Client()
client.username_pw_set("user", "xxxxxx")
client.on_connect = on_connect
client.on_message = on_message
client.connect("127.0.0.1", 1883, 60)

mythread = MyThread(name = "Count")
mythread.start()

client.loop_forever()

