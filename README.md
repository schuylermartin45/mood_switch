# mood_switch
Mood Switch is a Raspberry Pi-based project in which a Pi will control lighting and music from a stereo speaker remote.

# Required Tools
## Python Libraries
* **GMusicAPI**: TODO. Not sure if this will be used
    * Link: http://github.com/simon-weber/gmusicapi
* **GStreamer**: TODO. Not sure if this will be used
    * Link: http://gstreamer.freedesktop.org
* **evdev**: Provides Python bindings to the evdev interface in Linux. This
    interface can be used to handle generic input from system devices. Due to
    the lack of documentation that could be gathered from about the USB IR 
    receiver, this library was used to listen to input just from the remote.
    * Link: http://python-evdev.readthedocs.org/
## FLIRC Utilities
The FLIRC USB IR reciever used in this project was configured using software
provided by the manufacturer. It was advertised as having an open SDK available
to developers but that was not the case. Documentation on how I got this device
to work with the Pi is in a separae file, ```FLIRC_Notes.md```. The shortened
version of the story for primary README is that I eventually got the Pi to
interpret the signals from the remote as keyboard input.

