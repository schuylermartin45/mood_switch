#/usr/bin/python
from __future__ import print_function
# Linux's evdev module, wrapped for Python
from evdev import InputDevice, categorize, ecodes, list_devices, KeyEvent
# GStream object that runs music playing thread
import gobject
# Local imports
from musicservice import ServiceException
from localmusic import LocalService
from playback import Playback

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
    'up'        :   ecodes.KEY_W,       # ^
    'down'      :   ecodes.KEY_S,       # v
    'left'      :   ecodes.KEY_A,       # <
    'right'     :   ecodes.KEY_D,       # >
    'enter'     :   ecodes.KEY_ENTER,   # * (center)
    'return'    :   ecodes.KEY_X,       # Return
}

# Path for local music on this device
LOCAL_PATH = "local_music/"

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

def init_services():
    '''
    Initializes music service structures
    :return: Structure of Playback devices representing each available music
        service to the Pi
    '''
    services = []
    # attempt to initialize local service. If it fails, don't load the service
    try:
        services.append(Playback(LocalService(LOCAL_PATH)))
    except ServiceException:
        print("Warning: No local music found")
    # TODO Other services(?)
    return services

def main():
    '''
    Main execution point for testing
    '''
    # register the music playing thread
    music_loop = gobject.MainLoop()
    # see "MUSIC RUN LOOP" label below for further context
    gobject.threads_init()
    music_context = music_loop.get_context()

    # initialize input device (IR remote control)
    devices = dev_init()
    # init music services (Playback devices)
    services = init_services()
    # service in use
    cur_service = 0
    # check to see if a service is available
    if (len(services) < 1):
        print("Warning: No services loaded")
    # if start playing music!
    else:
        services[cur_service].playPause()
    
    # MUSIC RUN LOOP
    # Like many libraries used in this project, the Python bindings for 
    # GStreamer documentation are lacking. The suggested way to call the media
    # player is to execute the command "music_loop.run" but this causes a
    # blocking loop that prevents any of the remote control code from executing.
    # And it turns out you can't send this job to a new Python thread. The
    # GStreamer bindings execute C code directly while Python threads are
    # implemented at the interpretter level. Using the two in tandem will cause
    # the interpreter to lock-up. Hence why there is this ugly infinite while
    # loop surrounding this code block. All of this is better explained in this
    # link: http://www.jejik.com/articles/2007/01/python-gstreamer_threading
    #       _and_the_main_loop/
    while True:
        # play music by calling the media's context
        music_context.iteration(True)


        # read from specific device. This is a blocking loop but it only iterates
        # when input is coming from the device
        for event in devices[USB_IR_ID].read_loop():
            # trigger event on key release as this is the end of a button press
            # sequence (key_down -> key_hold(s) -> key_up)
            if ((event.type == ecodes.EV_KEY) and 
                    (event.value == KeyEvent.key_up)):
                # interpret command
                if (event.code == IR_MAP['light']):
                    print("Light") # TODO Actual command
                # ignore music playing commands if there aren't any available 
                # music services
                if (len(services) > 0):
                    if (event.code == IR_MAP['play']):
                        services[cur_service].playPause()
                    if (event.code == IR_MAP['next']):
                        services[cur_service].next()
                    if (event.code == IR_MAP['prev']):
                        services[cur_service].prev()
                    # TODO: Extra commands?

if __name__ == '__main__':
    main()
