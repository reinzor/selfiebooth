from time import strftime
from glob import glob
import os, sys

from random import randint

class ImageSaver():
    def __init__(self, raw_output_dir, logger):
        self._logger = logger
        self._raw_output_dir = raw_output_dir
        self._seq = 0

    def save(self, img):
        # Check how many image we have before storing
        num_before = len(glob("%s/*.jpeg" % self._raw_output_dir))

        # Generate path
        current_date = strftime("%Y_%m_%d_%H_%M_%S")
        img_path = "%s/%s_%d_%d.jpeg" % (self._raw_output_dir, current_date, self._seq, randint(0,1e10-1))

        # Store the image
        img_file = open(img_path, 'wb', 0)
        img.save(img_file, 'JPEG')
        img_file.flush()
        os.fsync(img_file)
        img_file.close()

        # Check how many image we have after storing
        num_after = len(glob("%s/*.jpeg" % self._raw_output_dir))

        # Some logging
        self._logger.info("Storing image to '%s', seq=%d, date=%s, num_before=%d, num_after=%d" % (img_path, self._seq, current_date, num_before, num_after) )

        if num_after != (num_before + 1):
            self._logger.error("Image was not saved correctly to the USB for some reason! Try to restart the machine or try another USB stick!")
            sys.exit(1)

        self._seq += 1
