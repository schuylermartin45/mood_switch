# mood_switch
Mood Switch is a Raspberry Pi-based project in which a Pi will control lighting and music from a stereo speaker remote.

# Required Tools
## Python Libraries
* **GMusicAPI**: TODO. GMusicAPI is an unofficial API to play songs from Google
    Music. As of writing, I had significant issues obtaining paths to music
    files using this API.
    * Link: http://github.com/simon-weber/gmusicapi
* **GStreamer**: Popular C library for handling media as stream information.
    This project uses the available Python bindings for the project.
    * Link: http://gstreamer.freedesktop.org
* **evdev**: Provides Python bindings to the evdev interface in Linux. This
    interface can be used to handle generic input from system devices. Due to
    the lack of documentation that could be gathered from about the USB IR 
    receiver, this library was used to listen to input just from the remote.
    * Link: http://python-evdev.readthedocs.org/

## Dependencies
* bluetooth, bluez, and alsa

These drivers/scripts/audio frameworks are used to pipe audio from gstreamer
over a bluetooth dongle to a bluetooth receiver. There are many documents online
that describe how to set this up but I found the blog below to be vert helpful
    * Link: http://blog.whatgeek.com.pt/2014/04/raspberry-pi-bluetooth-wireless-speaker/
* FLIRC Utilities

The FLIRC USB IR reciever used in this project was configured using software
provided by the manufacturer. It was advertised as having an open SDK available
to developers but that was not the case. Documentation on how I got this device
to work with the Pi is in a separae file, ```FLIRC_Notes.md```. The shortened
version of the story for primary README is that I eventually got the Pi to
interpret the signals from the remote as keyboard input.

