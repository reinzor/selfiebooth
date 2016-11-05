#!/usr/bin/env python

from selfiebooth import Selfiebooth
from load_usb import load_usb

# Mounting point
usb_mount = "/mnt/usb"

# Blocking until proper usb is inserted
config = load_usb(usb_mount)

# Run that thing
boot = Selfiebooth(config, usb_mount)
boot.run()
