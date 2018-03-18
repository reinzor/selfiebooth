# Selfiebooth Baas van Horst aan de Maas

![Illustration Selfiebooth](illustration.png)
Python code and assets Selfiebooth Baas van Horst aan de Maas.

## Hardware setup

### 1. Camera module

Connect raspberry PI camera module to board

### 2. GPIO setup for button

TODO: Add readme for GPIO setup (hardware)

## Software setup

### 1. Prepare raspberry pi image

- Raspbian (tested with ![Jessie lite](http://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2017-07-05/2017-07-05-raspbian-jessie-lite.zip)) installation on raspberry pi. Put a `ssh` file in the SD card boot partition to enable ssh server (to enable remote set-up).

### 2. Clone this repository

    sudo apt-get -y update && sudo apt-get install -y git
    git clone https://github.com/reinzor/selfieboot.git ~/selfiebooth

### 3. Run the install script

    ./install

## Configuration file 
The app searches for a USB stick that is inserted to the pi. If a config folder exists with a config.yaml, it will try to load this configuration. If none is found the default_config will be copied to the USB. If another config
directory existed; a backup will be created. 

### Config file parameters
- bottom_image: image path
- top_image: image path
- flash_image: image path
- countdown_images: list of image paths, every image takes 1 second
- screensaver_images: list of image paths
- flash_time: time in secs
- freeze_time: time in secs
- screensaver_time: time in secs
- screensaver_slide_time: time in secs
- screen_width: pixel size
- screen_height: pixel size

All specified paths are relative to the config file
