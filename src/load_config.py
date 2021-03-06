import os
import yaml


class Config():
    bottom_image = None
    top_image = None
    flash_image = None
    overlay_image = None
    countdown_images = None
    screensaver_images = None

    flash_time = None
    freeze_time = None
    screensaver_time = None 
    screensaver_slide_time = None 

    screen_width = None
    screen_height = None

    def __init__(self):
        pass

    def __str__(self):
        string = "Config:\n---------------"
        for member in dir(self):
            if member[0] != "_":
                string += "\n%s = %s" % (member, getattr(self, member))
        return string

    def valid(self):
        # Check if all images exist
        images = [self.bottom_image, self.top_image, self.flash_image, self.overlay_image] + self.countdown_images + self.screensaver_images
        for image in images:
            if not os.path.exists(image):
                print "Image '%s' does not exist" % image
                return False

        if self.flash_time <= 0 or self.flash_time > 100 or self.freeze_time <= 0 or self.freeze_time > 100 or self.flash_time > self.freeze_time:
            print "Invalid flash_time or freeze time (%f,%f). Both should be > 0 and < 100 and freeze_time > flash_time" % (self.flash_time, self.freeze_time)
            return False

        if self.screen_width <= 0 or self.screen_height <= 0:
            print "Invalid screen_width or screen_height (%d,%d)" % (self.screen_width, self.screen_height)
            return False

        if self.screensaver_time <= 0 or self.screensaver_slide_time <= 0:
            print "Invalid screensaver_time or screensaver_slide_time (%d,%d), should both be larger than 0" % (self.screensaver_time, self.screensaver_slide_time)
            return False

        return True


def load_config(path):

    print "Trying to load the configuration @ '%s'"%path

    config_filename = os.path.abspath(path)
    config_dirname = os.path.dirname(config_filename)

    config = Config()

    try:
        with open(config_filename, 'r') as stream:
            try:
                cfg = yaml.load(stream)

                # Check if we have everything in the config
                try: 
                    config.bottom_image = "%s/%s"%(config_dirname, cfg['bottom_image'])
                    config.top_image = "%s/%s"%(config_dirname, cfg['top_image'])
                    config.flash_image = "%s/%s"%(config_dirname, cfg['flash_image'])
                    config.overlay_image = "%s/%s"%(config_dirname, cfg['overlay_image'])
                    config.countdown_images = ["%s/%s"%(config_dirname, i) for i in cfg['countdown_images']]
                    config.screensaver_images = ["%s/%s"%(config_dirname, i) for i in cfg['screensaver_images']]

                    config.flash_time = float(cfg['flash_time'])
                    config.freeze_time = float(cfg['freeze_time'])
                    config.screensaver_time = float(cfg['screensaver_time'])
                    config.screensaver_slide_time = float(cfg['screensaver_slide_time'])

                    config.screen_width = int(cfg['screen_width'])
                    config.screen_height = int(cfg['screen_height'])

                    if config.valid():
                        return config

                except Exception as e:
                    print "Invalid configuration file. Key %s not present." % str(e)
            except:
                print "Invalid yaml, could not parse config [%s]" % config_filename
    except IOError as e:
        print "Could not open configuration file: %s" % e
    return None
