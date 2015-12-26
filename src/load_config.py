import os
import yaml

class Config():
    bottom_image = None
    top_image = None
    flash_image = None
    countdown_images = None
    screensaver_images = None

    flash_time = None
    freeze_time = None
    screensaver_time = None 
    screensaver_slide_time = None 

    screen_width = None
    screen_height = None

    def __str__(self):
        string = "Config:\n---------------"
        for member in dir(self):
            if member[0] != "_":
                string += "\n%s = %s" % (member, getattr(self, member))
        return string

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
                    config.countdown_images = ["%s/%s"%(config_dirname, i) for i in cfg['countdown_images']]
                    config.screensaver_images = ["%s/%s"%(config_dirname, i) for i in cfg['screensaver_images']]

                    config.flash_time = float(cfg['flash_time'])
                    config.freeze_time = float(cfg['freeze_time'])
                    config.screensaver_time = float(cfg['screensaver_time'])
                    config.screensaver_slide_time = float(cfg['screensaver_slide_time'])

                    config.screen_width = int(cfg['screen_width'])
                    config.screen_height = int(cfg['screen_height'])

                    return config
                except Exception as e:
                    print "Invalid configuration file. Key %s not present." % str(e)
            except:
                print "Invalid yaml, could not parse config [%s]" % config_filename
    except IOError as e:
        print "Could not open configuration file: %s" % e
    return None
