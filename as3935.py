#!/usr/local/bin/python3

from RPi_AS3935 import RPi_AS3935
import time
import datetime
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as paho
import signal
import sys

start_time = 0
now = 0
light = 0
first = True
pin = 24
debug = False

def on_connect(client, userdata, flags, rc):
  if debug:
    print("CONNACK received with code %d." % (rc))


def handle_interrupt(channel):
  time.sleep(0.003)
  global sensor
  global alert
  global light
  global start_time
  global first
  reason = sensor.get_interrupt()
  if reason == 0x01:
    if debug:
      print ("Noise level too high  adjusting")
    sensor.raise_noise_floor()
  elif reason == 0x04:
    if debug:
      print ("Disturber detected - masking")
    sensor.set_mask_disturber(True)
  elif reason == 0x08:
    distance = sensor.get_distance()
    if debug:
      print ("lightning!")
      print ("It was " + str(distance) + "km away.")
    light += 1
    if first:
      start_time = time.time()
      first = False
    count()
    #Trigger an alert if at least 4 lighting detected in the last minute
    if (light > 4 and alert):
      lightsensor()
      alert = False
      light = 0
      first = True

def lightsensor():
  (rc, mid) = client.publish("sensor/sroke", distance, qos=1)


def count():
  global start_time
  global alert
  global first
  global light
  now = time.time()
  if (now - start_time) < 60:
    alert = True
  if (now - start_time) > 60:
    first = True
    light = 0
    alert = False

def signal_handler(signal, frame):
  print('You pressed Ctrl+C!')
  sys.exit(1)

#MQTT
client = paho.Client()
client.username_pw_set("user", "XXXXXXX")
client.on_connect = on_connect
client.connect("127.0.0.1", 1883)
client.loop_start()

#GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN)
GPIO.add_event_detect(pin, GPIO.RISING, callback=handle_interrupt)

#Sensor
sensor = RPi_AS3935(address=0x03, bus=1)
sensor.calibrate(tun_cap=0x0F)
sensor.set_indoors(True)
sensor.set_noise_floor(0)

#SIGCATCH
signal.signal(signal.SIGINT, signal_handler)

if debug:
  print ("Waiting for lightning")

while True:
  time.sleep(1.0)
