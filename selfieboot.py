#!/usr/bin/python

import os.path
import sys

if len(sys.argv) == 1 and not os.path.isfile("/home/pi/selfieboot/images/alive"):
    print "ERROR: NO USB STICK WITH ALIVE FILE FOUND IN 'images' FOLDER"
    sys.exit(1)

import picamera
import io
from PIL import Image
from time import sleep, time
from collections import deque

# GPIO
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, GPIO.PUD_UP)
GPIO.add_event_detect(17, GPIO.FALLING)

# PARAMS
ROOT = "/home/pi/selfieboot/"
COUNTDOWN_TIME = 4
FREEZE_TIME = 4
FLASH_TIME = 1
SCREENSAVER_TIME = 60
SCREENSAVER_SLIDE_TIME = 10

# vars

screen_width_ = 1024
screen_height_ = 768

class Selfieboot(picamera.PiCamera):
    _time_last_press = 0
    _screensavers = deque()
    _screensaver_overlay = None

    def add_img_overlay(self, filename, where=None, fullscreen=False, alpha = 255, layer = 99):
        if not where or where != "top" or where != "bottom":
            x = 0
            y = 0

        img = Image.open(filename)

        width = img.size[0]
        height = img.size[1]

        if where == "bottom":
            x = 0
            y = screen_height_ - height

        pad = Image.new('RGB', ( ((width + 31) // 32) * 32, ((height + 15) // 16) * 16, ))
        pad.paste(img, (0, 0))

        return self.add_overlay(pad.tostring(), 
                size=img.size, 
                fullscreen=fullscreen,
                window=[x, y, width, height ], 
                alpha=alpha, 
                layer=layer)

    def add_screensaver(self, path):
        self._screensavers.appendleft(path)

    def check_screensaver(self):
        if time() - self._time_last_press > SCREENSAVER_TIME:
            self._screensavers.rotate()
            screensaver = self._screensavers[0]

            slide_start_time = time()

            if self._screensaver_overlay:
                tmp_screensaver_overlay = self.add_img_overlay(screensaver, layer = 10)
                self.remove_overlay(self._screensaver_overlay)
                self._screensaver_overlay = tmp_screensaver_overlay
            else:
                self._screensaver_overlay = self.add_img_overlay(screensaver, layer = 10)

            while time() - slide_start_time < SCREENSAVER_SLIDE_TIME:
                if self.push_button_pressed():
                    if self._screensaver_overlay:
                        self.remove_overlay(self._screensaver_overlay)
                        self._screensaver_overlay = None
                    break

    def make_picture(self):
        countdown_overlay_time = None
        countdown_overlay = None

        press_time = time()
        while time() - press_time < COUNTDOWN_TIME:
            time_left = COUNTDOWN_TIME - int(time()-press_time)
            if countdown_overlay_time != time_left:
                countdown_overlay_time = time_left
                if countdown_overlay:
                    tmp_countdown_overlay = self.add_img_overlay(ROOT + "assets/countdown%d.png"%time_left, layer = 11)
                    self.remove_overlay(countdown_overlay)
                    countdown_overlay = tmp_countdown_overlay
                else:
                    countdown_overlay = self.add_img_overlay(ROOT + "assets/countdown%d.png"%time_left, layer = 11)

            self.push_button_pressed(always_false=True)

        flash_overlay = self.add_img_overlay(ROOT + "assets/white.png", layer = 14)

        self.remove_overlay(countdown_overlay)

        # Take picture 
        stream = io.BytesIO()
        self.capture(stream, format="jpeg")
        stream.seek(0)
        img = Image.open(stream)

        width = img.size[0]
        height = img.size[1]

        pad = Image.new('RGB', ( ((width + 31) // 32) * 32, ((height + 15) // 16) * 16, ))
        pad.paste(img, (0, 0))

        capture_overlay = self.add_overlay(pad.tostring(), size=img.size, fullscreen=True, alpha=255, layer=13)

        start_freeze_time = time()
        while time() - start_freeze_time < FREEZE_TIME:
            duration = time() - start_freeze_time

            if duration < FLASH_TIME:
                alpha = int ( ( (FLASH_TIME - duration) / FLASH_TIME ) * 255 )
                flash_overlay.alpha = alpha

            self.push_button_pressed(always_false=True)

        self.remove_overlay(flash_overlay)
        self.remove_overlay(capture_overlay)

        # Store the image
        img.save(ROOT + "images/%d.jpeg"%int(press_time), "JPEG")

        self._time_last_picture = time()

    def push_button_pressed(self, always_false=False):
        sleep(.01)
        if GPIO.event_detected(17) and time() - self._time_last_press > 1.0 and not always_false:
            self._time_last_press = time()
            return True

        return False

with Selfieboot() as boot:
    boot.resolution = (1280, 720)
    boot.framerate = 24
    boot.start_preview()

    top_layer = boot.add_img_overlay(ROOT + "assets/top.png", where="top", layer=3)
    bottom_layer = boot.add_img_overlay(ROOT + "assets/bottom.png", where="bottom", layer=4)

    boot.add_screensaver(ROOT + "assets/slide1.png")
    boot.add_screensaver(ROOT + "assets/slide2.png")
    boot.add_screensaver(ROOT + "assets/slide3.png")
    boot.add_screensaver(ROOT + "assets/slide4.png")

    # Run it
    while True:
        # Always check the pushbutton press
        if boot.push_button_pressed():
            boot.make_picture()

        # Check the screensaver
        boot.check_screensaver()
