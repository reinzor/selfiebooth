#!/usr/bin/python

import picamera
from PIL import Image
from time import sleep

class Camera(picamera.PiCamera):
    def add_img_overlay(self, filename, alpha = 255, layer = 99):
        img = Image.open(filename)
        pad = Image.new('RGBA', ( ((img.size[0] + 31) // 32) * 32, ((img.size[1] + 15) // 16) * 16, ))
        pad.paste(img, (0, 0))

        return camera.add_overlay(pad.tostring(), size=img.size, alpha=alpha, layer=layer)

with Camera() as camera:
    camera.resolution = (1280, 720)
    camera.framerate = 24
    camera.start_preview()

    # Wait indefinitely until the user terminates the script
    while True:
        o = camera.add_img_overlay("assets/slide1.png")
        sleep(1)
        camera.remove_overlay(o)
        sleep(1)
        
