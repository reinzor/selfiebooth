#!/usr/bin/python

# from selfieboot import Selfieboot

import sys, os
import yaml

if len(sys.argv) < 2 or sys.argv[1][-5:] != ".yaml":
    print "Usage: python app.py [path_to_config.yaml]"
    sys.exit(1)

config_filename = os.path.abspath(sys.argv[1])
config_dirname = os.path.dirname(config_filename)

try:
    with open(config_filename, 'r') as stream:
        try:
            cfg = yaml.load(stream)
        except:
            print "Invalid yaml, could not parse config [%s]" % config_filename
            sys.exit()

        # Check if we have everything in the config
        bottom_image = "%s/%s"%(config_dirname, cfg['bottom_image'])
        top_image = "%s/%s"%(config_dirname, cfg['top_image'])
        flash_image = "%s/%s"%(config_dirname, cfg['flash_image'])
        countdown_images = ["%s/%s"%(config_dirname, i) for i in cfg['countdown_images']]
        screensaver_images = ["%s/%s"%(config_dirname, i) for i in cfg['screensaver_images']]

        flash_time = float(cfg['flash_time'])
        freeze_time = float(cfg['freeze_time'])

        screensaver_time = float(cfg['screensaver_time'])
        screensaver_slide_time = float(cfg['screensaver_slide_time'])

        # Screen specific things
        screen_width = int(cfg['screen_width'])
        screen_height = int(cfg['screen_height'])

        # Output
        raw_output_dir = "%s/%s"%(config_dirname, cfg['raw_output_dir'])
        overlay_image = "%s/%s"%(config_dirname, cfg['overlay_image'])
        overlayed_output_dir = "%s/%s"%(config_dirname, cfg['overlayed_output_dir'])  

        with Selfieboot(screen_width, 
                        screen_height
                        bottom_image,
                        top_image,
                        flash_image,
                        flash_time,
                        freeze_time,
                        screensaver_time,
                        screensaver_slide_time,
                        raw_output_dir,
                        overlay_image,
                        overlayed_output_dir) as boot:

            boot.add_screensaver(ROOT + "assets/slide1.png")
            boot.add_screensaver(ROOT + "assets/slide2.png")
            boot.add_screensaver(ROOT + "assets/slide3.png")
            boot.add_screensaver(ROOT + "assets/slide4.png")

            boot.run()

except IOError as e:
    print "Could not open configuration file: %s" % e