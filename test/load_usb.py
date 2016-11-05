#!/usr/bin/env python

from selfiebooth.load_usb import load_usb
import sys

if len(sys.argv) < 2:
    print "Usage: load_usb.py [mounting_point]"
    sys.exit(1)

cfg = load_usb(sys.argv[1])
print cfg
