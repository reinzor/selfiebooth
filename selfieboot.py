#!/usr/bin/python

import picamera
from PIL import Image
from time import sleep

screen_width = 1024
screen_height = 768

class Camera(picamera.PiCamera):
    def add_img_overlay(self, filename, where=None, alpha = 255, layer = 99):
        if not where or where != "top" or where != "bottom":
            x = 0
            y = 0

        img = Image.open(filename)

        width = img.size[0]
        height = img.size[1]

        if where == "bottom":
            x = 0
            y = screen_height - height

        pad = Image.new('RGB', ( ((width + 31) // 32) * 32, ((height + 15) // 16) * 16, ))
        pad.paste(img, (0, 0))

        return camera.add_overlay(pad.tostring(), 
                size=img.size, 
                fullscreen=False,
                window=[x, y, width, height ], 
                alpha=alpha, 
                layer=layer)

with Camera() as camera:
    camera.resolution = (1280, 720)
    camera.framerate = 24
    camera.start_preview()

    top_layer = camera.add_img_overlay("assets/overlay.png", where="top", layer=3)
    bottom_layer = camera.add_img_overlay("assets/overlay.png", where="bottom")

    # Wait indefinitely until the user terminates the script
    while True:
        sleep(1)
