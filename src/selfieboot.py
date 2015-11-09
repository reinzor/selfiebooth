import io, os
from PIL import Image
from time import sleep, time
from collections import deque
from random import shuffle

# RPI stuff
import picamera
import RPi.GPIO as GPIO

class Selfieboot(picamera.PiCamera):

    def __init__(self, 
                 screen_width, 
                 screen_height,
                 bottom_image,
                 top_image,
                 flash_image,
                 countdown_images,
                 screensaver_images,
                 flash_time,
                 freeze_time,
                 screensaver_time,
                 screensaver_slide_time,
                 raw_output_dir,
                 overlay_image,
                 overlayed_output_dir):

        # Call the picamera constructor
        super(Selfieboot, self).__init__()

        # Picamera setup
        self.resolution = (screen_width, screen_height)
        self.framerate = 24
        self.start_preview()

        self._top_overlay = self._add_img_overlay(top_image, where="top", layer=3)
        self._bottom_overlay = self._add_img_overlay(bottom_image, where="bottom", layer=4)
        self._flash_overlay = self._add_img_overlay(flash_image, layer=999)

        self._time_last_press = 0
    
        self._screensaver_overlays = [self._add_img_overlay(screensaver_image, layer=100+idx) for idx, screensaver_image in enumerate(screensaver_images)]
        self._countdown_overlays = [self._add_img_overlay(countdown_image, layer=200+idx) for idx, countdown_image in enumerate(countdown_images)]

        self._flash_time = flash_time
        self._freeze_time = freeze_time
        self._screensaver_time = screensaver_time
        self._screensaver_slide_time = screensaver_slide_time

        self._raw_output_dir = raw_output_dir
        self._overlay_image = overlay_image # TODO, use this one
        self._overlayed_output_dir = overlayed_output_dir

        # Check if folders exist
        if not os.path.isdir(raw_output_dir):
            print "Raw output dir %s does not exist!" % raw_output_dir
            sys.exit()
        if not os.path.isdir(overlayed_output_dir):
            print "Overlayed output dir %s does not exist!" % overlayed_output_dir
            sys.exit()

        self._setup_gpio()   

        self._setup_overlays()     

    def _setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.IN, GPIO.PUD_UP)
        GPIO.add_event_detect(17, GPIO.FALLING)

    def _setup_overlays(self):
        self._flash_layer.opacity = 0
        for overlay in self._screensaver_overlays + self._countdown_overlays:
            overlay.opacity = 0

    def _add_img_overlay(self, filename, where=None, fullscreen=False, alpha = 255, layer = 99):
        if not where or where != "top" or where != "bottom":
            x = 0
            y = 0

        try:
            img = Image.open(filename)
        except Exception as e:
            print e
            sys.exit()

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
            screensavers[0].opacity = 255

            while not self._push_button_pressed():
                if time() - slide_start_time > self._screensaver_slide_time:
                    screensavers[0].opacity = 0
                    screensavers.rotate()
                    screensavers[0].opacity = 255
                    slide_start_time = time()

            screensavers[0].opacity = 255

    def _make_picture(self):
        # Countdown
        for overlay in self._countdown_overlays:
            overlay.opacity = 255
            sleep(1)
            overlay.opacity = 0

        # Take picture 
        stream = io.BytesIO()
        self.capture(stream, format="jpeg")
        stream.seek(0)
        img = Image.open(stream)

        # Picture to overlay
        pad = Image.new('RGB', ( ((img.size[0] + 31) // 32) * 32, ((img.size[1] + 15) // 16) * 16, ))
        pad.paste(img, (0, 0))
        capture_overlay = self.add_overlay(pad.tostring(), size=img.size, fullscreen=True, alpha=255, layer=13)

        start_freeze_time = time()
        while time() - start_freeze_time < self._freeze_time:
            duration = time() - start_freeze_time

            if duration < self._flash_time:
                flash_overlay.alpha = int ( ( (self._flash_time - duration) / self._flash_time ) * 255 )

            self.push_button_pressed(always_false=True)

        self._flash_overlay.opacity = 0
        self.remove_overlay(capture_overlay)

        # Store the image
        img.save("%s/images/%d.jpeg" % (self._raw_output_dir, int(start_freeze_time)), "JPEG")

        # TODO: Create overlay image and save to overlayed_output_dir

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
