#/usr/bin/python
from __future__ import print_function
import threading
import os
from os.path import *
# Linux's evdev module, wrapped for Python
from evdev import InputDevice, categorize, ecodes, list_devices, KeyEvent
# GStream object that runs music playing thread
import gobject
import gst
# To detect bluetooth connectivity
import dbus
from dbus.mainloop.glib import DBusGMainLoop
# Local imports
from musicservice import ServiceException
from localmusic import LocalService
from radiomusic import RadioService
from playback import Playback
from servocontrol import Switch

'''
remote.py
Python program for interpretting remote input
@author: Schuyler Martin <schuylermartin45@gmail.com>
'''
__author__ = "Schuyler Martin"

# Hardware ID of the USB IR device
USB_IR_ID = "20a0:0004"
# Bluetooth device ID (used for detecting connection/disconnection)
BT_DEV_ID = "48_E2_44_F3_E7_07"
# Upon disconnecting with the bluetooth device, kill the app so that the
# wrapping daemon script can start it back up
BT_ERROR_CODE = 22
# Mapping enumerated actions to the IR buttons from the remote
IR_MAP = {
    # Command   : USB firmware mapping  # Actual button on remote
    'light'     :   ecodes.KEY_SPACE,   # Display
    'play'      :   ecodes.KEY_UP,      # >/||
    'next'      :   ecodes.KEY_RIGHT,   # >>|
    'prev'      :   ecodes.KEY_LEFT,    # |<<
    'stop'      :   ecodes.KEY_C,       # []
    'up'        :   ecodes.KEY_W,       # ^
    'down'      :   ecodes.KEY_S,       # v
    'left'      :   ecodes.KEY_A,       # <
    'right'     :   ecodes.KEY_D,       # >
    'enter'     :   ecodes.KEY_ENTER,   # * (center)
    'return'    :   ecodes.KEY_X,       # Return
}

class Remote():
    '''
    Class for "Remote" which controls most of the runtime code
    '''
    def __init__(self, run_dir):
        '''
        Constructor
        :param: run_dir Path for the local music service's directory
        '''
        self.run_dir = run_dir
        # register the music playing thread
        self.main_loop = gobject.MainLoop()
        # see "MUSIC RUN LOOP" label below for further context
        gobject.threads_init()

        # initialize input device (IR remote control)
        self.devices = self.dev_init()
        # input thread for remote_control
        self.in_thread = threading.Thread(target=self.run_input)
        # setting this variable guarantees the interpetter will handle thread
        # clean-up on killing this program
        self.in_thread.daemon = True
        # service in use
        self.cur_id = 0
        # init music services (Playback devices)
        self.services = self.init_services()
        # check to see if a service is available
        if (len(self.services) < 1):
            print("Warning: No services loaded")
        # if start playing music!
        else:
            # initialize event handling
            bus = self.player.get_bus()
            bus.enable_sync_message_emission()
            bus.add_signal_watch()
            bus.connect("message", self.msgEvent)
            self.services[self.cur_id].playPause()
    
    def hwd_id(self, i):
        '''
        Formats part of a hardware id (to 4 hex digits)
        :param: i Decimal integer
        :return: 4-digit hex string (with no 0x prefix)
        '''
        hexStr = hex(i)[2:]
        while len(hexStr) < 4:
            hexStr = "0" + hexStr
        return hexStr

    def dev_init(self):
        '''
        Initializes information regarding available input devices
        :return: Dictionary of input devices, indexed by hardware id
        '''
        devices = {}
        # take the device listing and convert it to a dictionary, indexed by the
        # vendor_id:product_id (as is seen via lsusb and other tools)
        for dev in list_devices():
            dev = InputDevice(dev)
            v_id = self.hwd_id(dev.info[1])
            p_id = self.hwd_id(dev.info[2])
            id = str(v_id) + ":" + str(p_id)
            devices[id] = dev
        return devices

    def msgEvent(self, bus, message):
        '''
        Handles "message" events from the music player's bus
        :param: bus Player communication bus
        :param: message Message object from bus
        '''
        # if the song ends or encounters an error, try the next song
        if ((message.type == gst.MESSAGE_EOS) or 
                (message.type == gst.MESSAGE_ERROR)):
            # if the TTS file is done playing, play the current song
            if (self.services[self.cur_id].pl_TTS):
                self.services[self.cur_id].pl_TTS = False
                self.services[self.cur_id].play()
            elif (self.services[self.cur_id].shuffle_TTS):
                self.services[self.cur_id].shuffle_TTS = False
                self.services[self.cur_id].play()
            # else advance to the next song
            else:
                self.services[self.cur_id].next()

    def init_services(self):
        '''
        Initializes music service structures
        :return: Structure of Playback devices representing each available music
            service to the Pi
        '''
        services = []
        # attempt to initialize local service. If it fails, don't load that
        # service
        try:
            cachePath = self.run_dir + ".mood_switch_cache/"
            # make directory if missing
            if not(os.path.exists(cachePath)):
                os.makedirs(cachePath)
            # make services
            local_service = LocalService(self.run_dir + "local_music/")
            radio_service = RadioService()
            # init a single player for all music services
            self.player = Playback.constructPlayer()
            # add services
            services.append(Playback(self.player, local_service, cachePath))
            # remote services, such as the radio service will constantly
            # throw errors if there is no X11 (although they appear to work)
            # So they are disabled if X11 is missing
            if (os.environ.get("DISPLAY") != None):
                services.append(
                    Playback(self.player, radio_service, cachePath))
        except ServiceException:
            print("Warning: No local music found")
        return services

    def nextService(self):
        '''
        Moves to the next music service
        :return: New service id
        '''
        # kill current song playing
        self.services[self.cur_id].stop()
        if (self.cur_id == (len(self.services) - 1 )):
            self.cur_id = 0
        else:
            self.cur_id += 1
        self.services[self.cur_id].play()
        return self.cur_id

    def prevService(self):
        '''
        Moves to the previous music service
        :return: New service id
        '''
        # kill current song playing
        self.services[self.cur_id].stop()
        if (self.cur_id == 0):
            self.cur_id = len(self.services) - 1
        else:
            self.cur_id -= 1
        self.services[self.cur_id].play()
        return self.cur_id

    def run_input(self):
        # loop input reading from device
        for event in self.devices[USB_IR_ID].read_loop():
            # trigger event on key release as this is the end of a button press
            # sequence (key_down -> key_hold(s) -> key_up)
            if ((event != None) and (event.type == ecodes.EV_KEY) and 
                    (event.value == KeyEvent.key_up)):
                # interpret command
                if (event.code == IR_MAP['light']):
                    pass
                # ignore music playing commands if there aren't any available 
                # music services
                if (len(self.services) > 0):
                    # === Basic playback Control ===
                    if (event.code == IR_MAP['play']):
                        self.services[self.cur_id].playPause()
                    elif (event.code == IR_MAP['next']):
                        self.services[self.cur_id].next()
                    elif (event.code == IR_MAP['prev']):
                        self.services[self.cur_id].prev()
                    # === Moving bewteen playlists ===
                    elif (event.code == IR_MAP['left']):
                        self.services[self.cur_id].prevPl()
                    elif (event.code == IR_MAP['right']):
                        self.services[self.cur_id].nextPl()
                    # === Moving bewteen services ===
                    # currently there is only one service available
                    elif (event.code == IR_MAP['up']):
                        self.nextService()
                    elif (event.code == IR_MAP['down']):
                        self.prevService()
                    # shuffle current playlist
                    elif (event.code == IR_MAP['stop']):
                        self.services[self.cur_id].shuffle()
                    # Ignore other inputs until they are written
                    else:
                        pass

    def run(self):
        '''
        Primary runtime control
        '''
        # start looking for input in a separate thread. This allows us to do
        # some smarter control with the music playback
        self.in_thread.start()
        # main runtime loop
        self.main_loop.run()

def conEvent(iface=None, mbr=None, path=None):
    '''
    Event handling connection/disconnection of the bluetooth device
    :param: iface Hardware string representing the interface
    :param: mbr Type of event
    :param: path Hardware string representing the device ID
    '''
    if ((iface == "org.bluez.AudioSink") and (path.find(BT_DEV_ID))):
        if (mbr == "Disconnected"):
            remote.main_loop.quit()
            # this is by far the dirtiest way to kill a python script
            # BUT the signal handler raises an exception when sys.exit() is
            # used here and that doesn't properly return the correct error code
            # to OS (to be picked up by the wrapping shell scripts)
            os._exit(BT_ERROR_CODE)

def bt_init():
    '''
    "Initialize" the bluetooth device by setting up a method for detecting
        that the device has been connected/disconnected
    '''
    # handle connection/disconnection scenarios by looking at the dbus
    # and the bluetooth adapter
    btBus = dbus.SystemBus(mainloop=DBusGMainLoop())
    btObj = btBus.get_object("org.bluez", "/")
    iface = dbus.Interface(btObj, "org.bluez.Manager")
    adptrPath = iface.DefaultAdapter()
    btDev = btBus.get_object("org.bluez", adptrPath + "/dev_" + BT_DEV_ID)
    # setup signalling events
    btDev.connect_to_signal("Disconnected", conEvent, 
        interface_keyword="iface", member_keyword="mbr", 
        path_keyword="path")
    btDev.connect_to_signal("Connected", conEvent, 
        interface_keyword="iface", member_keyword="mbr", 
        path_keyword="path")

if __name__ == '__main__':
    # initialize listening to bluetooth connections
    bt_init()
    curDir = os.path.dirname(os.path.abspath(__file__)) + "/"
    remote = Remote(curDir)
    # start looking for input and start a playback loop
    remote.run()
