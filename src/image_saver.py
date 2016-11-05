from time import strftime
from glob import glob
import os
import sys

from PIL import Image
from random import randint


def overlay_image(image, overlay):
    img = Image.open(image, 'r')

    overlay_img = Image.open(overlay, 'r')
    has_alpha = overlay_img.mode == 'RGBA'
    if not has_alpha:
        raise Exception("The overlay image does not have an alpha channel! Overlay failed!")

    # Resize the overlay to match the img
    overlay_img = overlay_img.resize(img.size, Image.ANTIALIAS)

    # Now past the overlay on the img
    img.paste(overlay_img, (0, 0), overlay_img)

    # Create path
    parts = image.split("/")
    overlay_img_path = "/".join(parts[:-1] + ["overlayed_" + parts[-1]])

    # Store the image
    img_file = open(overlay_img_path, 'wb', 0)
    img.save(img_file, 'JPEG')
    img_file.flush()
    os.fsync(img_file)
    img_file.close()


class ImageSaver():
    def __init__(self, raw_output_dir, logger, overlay_image):
        self._logger = logger
        self._raw_output_dir = raw_output_dir
        self._seq = 0
        self._overlay_image = overlay_image

    def save(self, img):
        # Check how many image we have before storing
        num_before = len(glob("%s/*.jpeg" % self._raw_output_dir))

        # Generate path
        current_date = strftime("%Y_%m_%d_%H_%M_%S")
        img_path = "%s/%s_%d_%d.jpeg" % (self._raw_output_dir, current_date, self._seq, randint(0, 1e10-1))

        # Store the image
        img_file = open(img_path, 'wb', 0)
        img.save(img_file, 'JPEG')
        img_file.flush()
        os.fsync(img_file)
        img_file.close()

        # Try to overlay the image
        try:
            overlay_image(img_path, self._overlay_image)
        except Exception as e:
            self._logger("Failed to overlay the image: %s" % e)

        # Check how many image we have after storing
        num_after = len(glob("%s/*.jpeg" % self._raw_output_dir))

        # Some logging
        self._logger.info("Storing image to '%s', seq=%d, date=%s, num_before=%d, num_after=%d"
                          % (img_path, self._seq, current_date, num_before, num_after) )

        if num_after == num_before:
            self._logger.error("Image was not saved correctly to the USB for some reason! "
                               "Try to restart the machine or try another USB stick!")
            sys.exit(1)

        self._seq += 1
