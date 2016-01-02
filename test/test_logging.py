#!/usr/bin/python

from selfiebooth.logger import Logger
from time import sleep

logger = Logger(".")

for i in range(0,100):
    logger.info("Bla %d" % i)
    sleep(0.5)
