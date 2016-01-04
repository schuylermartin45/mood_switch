#/usr/bin/python
from __future__ import print_function
# Linux's evdev module, wrapped for Python
from evdev import InputDevice, categorize, ecodes, list_devices

'''
remote.py
Python program for interpretting remote input
@author: Schuyler Martin <schuylermartin45@gmail.com>
'''
__author__ = "Schuyler Martin"

# Hardware ID of the USB IR device
USB_IR_ID = "20a0:0004"
# Mapping enumerated actions to the IR buttons from the remote
IR_MAP = {
    # Command   : USB firmware mapping  # Actual button on remote
    'light'     :   ecodes.KEY_SPACE,   # Display
    'play'      :   ecodes.KEY_UP,      # >/||
    'next'      :   ecodes.KEY_RIGHT,   # >>|
    'prev'      :   ecodes.KEY_LEFT,    # |<<
}

def dev_init():
    '''
    Initializes information regarding available input devices
    :return: Dictionary of input devices, indexed by hardware id
    '''
    devices = {}
    # take the device listing and convert it to a dictionary, indexed by the
    # vendor_id:product_id (as is seen via lsusb and other tools)
    for dev in list_devices():
        dev = InputDevice(dev)
        
        v_id = hwd_id(dev.info[1])
        p_id = hwd_id(dev.info[2])
        id = str(v_id) + ":" + str(p_id)
        devices[id] = dev
    return devices

def hwd_id(i):
    '''
    Formats part of a hardware id (to 4 hex digits)
    :param: i Decimal integer
    :return: 4-digit hex string (with no 0x prefix)
    '''
    hexStr = hex(i)[2:]
    while len(hexStr) < 4:
        hexStr = "0" + hexStr
    return hexStr

def main():
    '''
    Main execution point for testing
    '''
    devices = dev_init()
    # read from specific device
    for event in devices[USB_IR_ID].read_loop():
        if event.type == ecodes.EV_KEY:
            print(categorize(event))

if __name__ == '__main__':
    main()
