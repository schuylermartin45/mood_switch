#/usr/bin/python
from __future__ import print_function
import threading
import os
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
from playback import Playback

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

class Remote():
    '''
    Class for "Remote" which controls most of the runtime code
    '''
    def __init__(self, local_path):
        '''
        Constructor
        :param: local_path Path for the local music service's directory
        '''
        self.local_path = local_path
        # register the music playing thread
        music_loop = gobject.MainLoop()
        # see "MUSIC RUN LOOP" label below for further context
        gobject.threads_init()
        self.music_context = music_loop.get_context()

        # initialize input device (IR remote control)
        self.devices = self.dev_init()
        # input thread for remote_control
        self.in_thread = threading.Thread(target=self.run_input)
        # setting this variable guarantees the interpetter will handle thread
        # clean-up on killing this program
        self.in_thread.daemon = True
        # init music services (Playback devices)
        self.services = self.init_services()
        # service in use
        self.cur_id = 0
        # Assume bluetooth is connected
        self.is_BT_Connect = True
        # check to see if a service is available
        if (len(self.services) < 1):
            print("Warning: No services loaded")
        # if start playing music!
        else:
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
            services.append(Playback(LocalService(self.local_path)))
        except ServiceException:
            print("Warning: No local music found")
        # TODO Other services(?)
        return services

    def nextService(self):
        '''
        Moves to the next music service
        :return: New service id
        '''
        # kill current song playing
        self.services[self.cur_id].pause()
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
        self.services[self.cur_id].pause()
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
                    print("Light") # TODO Actual command
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
        
        # MUSIC RUN LOOP
        # Like many libraries used in this project, the Python bindings for 
        # GStreamer documentation are lacking. The suggested way to call the
        # player is to execute the command "music_loop.run" but this causes a
        # blocking loop that prevents any of the controller code from running.
        # And it turns out you can't send this job to a new Python thread. The
        # GStreamer bindings execute C code directly while Python threads are
        # implemented at the interpretter level. Using the two in tandem will
        # cause the interpreter to lock-up. Hence why there is this ugly while-
        # true loop surrounding this code block. All of this is better explained
        # here: http://www.jejik.com/articles/2007/01/python-gstreamer_threading
        #       _and_the_main_loop/
        while self.is_BT_Connect:
            # play music by calling the media's context. Setting to false
            # prevents this from becoming a blocking call (one iteration is run)
            self.music_context.iteration(True)

    def conEvent(self, iface=None, mbr=None, path=None):
        '''
        Event handling connection/disconnection of the bluetooth device
        :param: iface Hardware string representing the interface
        :param: mbr Type of event
        :param: path Hardware string representing the device ID
        '''
        print(threading.current_thread())
        if ((iface == "org.bluez.AudioSink") and (path.find(BT_DEV_ID))):
            if (mbr == "Connected"):
                print("Connected")
            elif (mbr == "Disconnected"):
                print("Disconnected")
                self.is_BT_Connect = False
                curDir = os.path.dirname(os.path.abspath(__file__)) + "/" 
                self = Remote(curDir + "local_music/")
                self.run()

    def bt_init(self):
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
        btDev.connect_to_signal("Disconnected", self.conEvent, 
            interface_keyword="iface", member_keyword="mbr", 
            path_keyword="path")
        btDev.connect_to_signal("Connected", self.conEvent, 
            interface_keyword="iface", member_keyword="mbr", 
            path_keyword="path")

if __name__ == '__main__':
    # initialize listening to bluetooth connections
    curDir = os.path.dirname(os.path.abspath(__file__)) + "/"
    remote = Remote(curDir + "local_music/")
    #remote.bt_init()
    remote.run()
