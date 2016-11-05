#!/usr/bin/env python

import os.path
import sys
from time import sleep

# GPIO
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, GPIO.PUD_UP)
GPIO.add_event_detect(17, GPIO.FALLING)

while True:
    sleep(.01)
    if GPIO.event_detected(17):
        print "pressed" 

