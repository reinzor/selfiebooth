#!/usr/bin/env python

from selfiebooth.mount_usb import mount_usb
import sys

if len(sys.argv) < 2:
    print "Usage: mount_usb.py [mounting_point]"
    sys.exit(1)

mount_usb(sys.argv[1])