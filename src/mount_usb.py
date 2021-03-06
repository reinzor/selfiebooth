#!/usr/bin/python

import os, glob, time, socket


def _print_network_status():
    try:
        print "IP: %s" % str([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                                           if not ip.startswith("127.")][:1],
                                          [[(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close())
                                            for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]])
                              if l][0][0])
    except:
        print "Network unreachable"


def mount_usb(mounting_point):
    while True:
        usb_partitions = glob.glob("/dev/sd[a-z][0-9]")

        if len(usb_partitions) == 0:
            print "I did not find an usb-stick, please insert a valid preferably FAT32 formatted usb stick ..."
        else:
            for usb_partition in usb_partitions:
                cmd_mkdir = "mkdir -p %s" % mounting_point

                print "Creating mounting point @ %s (%s)"%(mounting_point, cmd_mkdir)
                if os.system(cmd_mkdir) == 0:
                    print "Succesfully created mounting point @ %s" % mounting_point
                else:
                    print "Failed to create mounting point"
                    continue

                cmd_umount = "umount %s" % mounting_point
                print "Unmounting possibly mounted partition (%s)" % cmd_umount
                os.system(cmd_umount)

                cmd_mount = "mount %s %s" % (usb_partition, mounting_point)
                print "Trying to mount USB partition %s" % (cmd_mount)

                if os.system(cmd_mount) == 0:
                    print "Succesfully mounted usb stick @ %s" % mounting_point
                    return
                else: 
                    print "Failed to mount usb stick :("

        sleep_seconds = 1
        print "Sleeping for %d seconds..." % sleep_seconds
        _print_network_status()
        time.sleep(sleep_seconds)
