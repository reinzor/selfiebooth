#!/usr/bin/env python

from selfiebooth.load_config import load_config
import sys

if len(sys.argv) < 2:
    print "Usage: load_config.py [config.yaml]"
    sys.exit(1)

print load_config(sys.argv[1])
