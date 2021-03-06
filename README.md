# mood_switch
Mood switch is a Raspberry Pi-based project that controls lighting (flips a 
lightswitch) and music from a stereo speaker remote.

## About
The basic premise is that the "mood switch" is it is a Raspberry Pi 
media system permanently mounted next to a room's lightswitch. The Pi is 
controlled by an IR stereo system remote. One button controls the lighting
in the room while other buttons control the music platform. The Pi plays
music over a bluetooth connected speaker, located elsewhere in the room.


This project is mostly written in Python. There are two provided Bash scripts
that "daemonize" the runtime of the mood switch program. It is designed to be 
persistent: if the bluetooth connection dies, the daemon scripts will detect 
that change and prep itself for when the Pi is reconnected to the speakers.
This "always on" approach makes the mood switch a very convenient music system.


**Note**: As of writing, the lightswitch feature is only partially implemented.
I have a test script that can move the servo on the Raspberry Pi.
However there are a few issues:
1. The servo I purchased does not have enough torque to turn the light switch.
2. When run as a background process/daemon, the Pi throws a GPIO exception
indicating that access to the GPIO pins are not available. This does not happen
if I run the program manually and indicates that the Pi prevents such access to
the GPIO board for security concerns. I'm not sure if there is much I can do at
this point to resolve this.

## Features
* **Plugins**: The system is designed to have "plugin" music services via an 
"interface". Currently there is one music service available that plays songs
locally off of the Pi. The hope is that other online streaming services can
be added down the line.
* **Intuitive**: Everything is controlled by a single IR remote with common
command mappings. For instance, you can switch between playlists by using the
left and right arrows on the remote, while up/down cycles through music
services.
* **Text to speech**: Due to the lack of a screen, the mood switch project
vocalizes important information to the user, such as which playlist is
currently playing and the current shuffle state.

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
* **Raspbian w/ X11**:
This project was written on/for a Raspberry Pi 2. I wanted this project to
run in a "text-only" environment but unfortunately I could not get Gstreamer 
to stream remotely without whining about not having X11 available. Odd, since
I was testing audio streams.
* **bluetooth, bluez, and alsa**: 
These drivers/scripts/audio frameworks are used to pipe audio from gstreamer
over a bluetooth dongle to a bluetooth receiver. There are many documents online
that describe how to set this up but I found the blog below to be vert helpful
    * Link: http://blog.whatgeek.com.pt/2014/04/raspberry-pi-bluetooth-wireless-speaker/
* **FLIRC Utilities**: 
The FLIRC USB IR reciever used in this project was configured using software
provided by the manufacturer. It was advertised as having an open SDK available
to developers but that was not the case. Documentation on how I got this device
to work with the Pi is in a separae file, ```FLIRC_Notes.md```. The shortened
version of the story for primary README is that I eventually got the Pi to
interpret the signals from the remote as keyboard input.
* **espeak**:
Text-to-speech synthesis used to alert the user which playlist is playing upon
switching playlists.
