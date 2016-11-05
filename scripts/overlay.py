#!/usr/bin/env python

import sys
from selfiebooth.image_saver import overlay_image

if len(sys.argv) < 3:
    print "Usage: overlay.py [overlay.png] [images...]"
    sys.exit(1)

overlay = sys.argv[1]
images = sys.argv[2:]

for image in images:
    print "Overlaying %s with %s" % (image, overlay)
    overlay_image(image, overlay)
