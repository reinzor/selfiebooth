#!/usr/bin/python

from selfieboot import Selfieboot
from load_usb import load_usb

import sys, os
import yaml

# Blocking until proper usb is inserted
config = load_usb()

# Run that thing
boot = Selfieboot(config, "/mnt/usb")
boot.run()
