#!/usr/bin/env python
# -*- coding: utf-8 -*-

## dependency: python-usb
import usb.core
import usb.util

## dependency: python-liblo (pyliblo)
import liblo

import time
import json
import os.path

from liveset.livesetconf import *

def run():
    port = 56418

    with open(settings_file) as data_file:
        settings = json.load(data_file) 


    idVendor  = int(settings['idVendor'], 16)
    idProduct = int(settings['idProduct'], 16)
    dataValueUSB = int(settings['dataValueUSB'])
    dataIndexUSB = int(settings['dataIndexUSB'])

    ## find the device
    dev = usb.core.find(idVendor=idVendor, idProduct=idProduct)
    if dev is None:
        raise ValueError('Device not found')

    # first endpoint
    interface = 0
    endpoint = dev[0][(0,0)][0]

    # if the OS kernel already claimed the device, which is most likely true
    # thanks to http://stackoverflow.com/questions/8218683/pyusb-cannot-set-configuration
    if dev.is_kernel_driver_active(interface) is True:
        # tell the kernel to detach
        dev.detach_kernel_driver(interface)
        # claim the device
        usb.util.claim_interface(dev, interface)

    while True:
        time.sleep(0.3)
        if os.path.exists(switchmode_file):
            with open(switchmode_file) as switchMode_file:
                switch_mode = switchMode_file.readlines()
        else:
            switch_mode = ["switchsubscene"]
        try:
            data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
            ## data from usb device
            if data[dataIndexUSB] == dataValueUSB:
                if switch_mode[0] == "switchscene":
                    liblo.send(port,  '/mididings/next_scene')
                if switch_mode[0] == "switchsubscene":	
                    liblo.send(port,  '/mididings/next_subscene')
        except usb.core.USBError as e:
            data = None
            if e.args == ('Operation timed out',):
                continue
    # release the device
    usb.util.release_interface(dev, interface)
    # reattach the device to the OS kernel
    dev.attach_kernel_driver(interface)

run()