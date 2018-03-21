#!/usr/bin/env python

from time import sleep
import RPi.GPIO as GPIO

BCM_PIN = 3

GPIO.setmode(GPIO.BCM)
GPIO.setup(BCM_PIN, GPIO.IN)
GPIO.add_event_detect(BCM_PIN, GPIO.FALLING)

while True:
    sleep(.01)
    if GPIO.event_detected(BCM_PIN):
        print "pressed" 

