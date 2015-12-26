#!/usr/bin/python

import os, time
from shutil import copytree, rmtree

from mount_usb import mount_usb
from load_config import load_config

def load_usb(usb_mount):
    # Blocking call untill usb stick can be mounted
    mount_usb(usb_mount)

    # Try to load the config on the usb stick
    config_dir = "%s/config" % usb_mount
    default_config_dir = "%s/../default_config" % os.path.dirname(os.path.realpath(__file__))
    config_path = "%s/config/config.yaml" % usb_mount

    config = load_config(config_path)
    while config is None:
        print "Failed to load config @ '%s'"%config_path

        # Check if we have a config folder inside our usb stick
        if os.path.isdir(config_dir):
            # Create a backup of the original config dir
            print "Creating a backup of the config directory"
            copytree(config_dir, "%s_backup_%s" % (config_dir, time.strftime("%Y_%m_%d_%H_%M")))

            # Remove the original config dir
            print "Removing the config directory on usb stick"
            rmtree(config_dir)

        # Copy the default_config to that directory
        print "Copying default config dir to config dir on usb stick..."
        copytree(default_config_dir, config_dir)

        config = load_config(config_path)

    print "Succesfully loaded usb_stick" 

    return config
