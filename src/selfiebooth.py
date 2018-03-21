import io
from PIL import Image
from time import sleep, time
from collections import deque
from random import shuffle

from logger import Logger
from image_saver import ImageSaver

# RPI stuff
import picamera
import RPi.GPIO as GPIO

BCM_PIN = 3


class Selfiebooth(picamera.PiCamera):

    def __init__(self, config, raw_output_dir):

        # Call the picamera constructor
        super(Selfiebooth, self).__init__()

        # Create logger
        self._logger = Logger(raw_output_dir)
        self._logger.info('Selfiebooth started')

        # Picamera setup
        self.resolution = (config.screen_width, config.screen_height)
        self.framerate = 24
        self.hflip = True
        self.start_preview()

        self._top_overlay = self._add_img_overlay(config.top_image, where="top", layer=4)
        self._bottom_overlay = self._add_img_overlay(config.bottom_image, where="bottom", layer=5)
        self._flash_overlay = self._add_img_overlay(config.flash_image, layer=255)

        self._time_last_press = 0

        self._screensaver_overlays = [self._add_img_overlay(screensaver_image, layer=50+idx)
                                      for idx, screensaver_image in enumerate(config.screensaver_images)]
        self._countdown_overlays = [self._add_img_overlay(countdown_image, layer=100+idx)
                                    for idx, countdown_image in enumerate(config.countdown_images)]

        self._flash_time = config.flash_time
        self._freeze_time = config.freeze_time
        self._screensaver_time = config.screensaver_time
        self._screensaver_slide_time = config.screensaver_slide_time

        self._image_saver = ImageSaver(raw_output_dir, self._logger, config.overlay_image)

        self._setup_gpio()

        self._setup_overlays()

    @staticmethod
    def _setup_gpio():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BCM_PIN, GPIO.IN)
        GPIO.add_event_detect(BCM_PIN, GPIO.FALLING)

    def _setup_overlays(self):
        self._flash_overlay.alpha = 0
        for overlay in self._screensaver_overlays + self._countdown_overlays:
            overlay.alpha = 0

    def _add_img_overlay(self, filename, where=None, fullscreen=False, alpha = 255, layer = 99):
        if not where or where != "top" or where != "bottom":
            x = 0
            y = 0

        img = Image.open(filename)

        width = img.size[0]
        height = img.size[1]

        if where == "bottom":
            x = 0
            y = self.resolution[1] - height

        pad = Image.new('RGB', ( ((width + 31) // 32) * 32, ((height + 15) // 16) * 16, ))
        pad.paste(img, (0, 0))

        return self.add_overlay(pad.tostring(),
                                size=img.size,
                                fullscreen=fullscreen,
                                window=[x, y, width, height ],
                                alpha=alpha,
                                layer=layer)

    def _check_screensaver(self):
        if time() - self._time_last_press > self._screensaver_time:
            # Create a deque from screensavers
            screensavers = deque(self._screensaver_overlays)
            shuffle(screensavers)

            slide_start_time = time()
            screensavers[0].alpha = 255

            while not self._push_button_pressed():
                if time() - slide_start_time > self._screensaver_slide_time:
                    screensavers[0].alpha = 0
                    screensavers.rotate()
                    screensavers[0].alpha = 255
                    slide_start_time = time()

            screensavers[0].alpha = 0

    def _make_picture(self):
        # Countdown
        for overlay in self._countdown_overlays:
            overlay.alpha = 255
            sleep(1)
            overlay.alpha = 0

        # Flash overlay
        self._flash_overlay.alpha = 255

        # Take picture
        stream = io.BytesIO()
        self.capture(stream, format="jpeg")
        stream.seek(0)
        img = Image.open(stream)

        # Picture to overlay
        pad = Image.new('RGB', ( ((img.size[0] + 31) // 32) * 32, ((img.size[1] + 15) // 16) * 16, ))
        pad.paste(img, (0, 0))
        capture_overlay = self.add_overlay(pad.tostring(), size=img.size, fullscreen=True, alpha=255, layer=3)

        start_freeze_time = time()
        while time() - start_freeze_time < self._freeze_time:
            duration = time() - start_freeze_time

            if duration < self._flash_time:
                self._flash_overlay.alpha = int ( ( (self._flash_time - duration) / self._flash_time ) * 255 )

            self._push_button_pressed(always_false=True)

        self._flash_overlay.alpha = 0
        self.remove_overlay(capture_overlay)

        self._image_saver.save(img)

        self._time_last_picture = time()

    def _push_button_pressed(self, always_false=False):
        sleep(.01)
        if GPIO.event_detected(17) and time() - self._time_last_press > 1.0 and not always_false:
            self._time_last_press = time()
            return True

        return False

    def run(self):
        # Run it
        while True:
            # Always check the pushbutton press
            if self._push_button_pressed():
                self._make_picture()

            # Check the screensaver
            self._check_screensaver()
