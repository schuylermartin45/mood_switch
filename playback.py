#/usr/bin/python
from __future__ import print_function
import os
from os.path import *
import subprocess
import pygst
import gst
# Local imports
from musicservice import ServiceException

'''
playback.py
Python class that controls playback
    Uses GStreamer w/ Python Bindings (gstreamer.freedesktop.org)
@author: Schuyler Martin <schuylermartin45@gmail.com>
'''
__author__ = "Schuyler Martin"

def mkTextSpeech(txt, fileName):
    '''
    Writes a text-to-speech file
    :param: text Text to synthesize
    :param: fileName File name to write-out to
    '''
    subprocess.call(["espeak", "-w" + fileName, text])

class Playback:
    '''
    Class that represents the playback system
    '''
    def __init__(self, service, cachePath):
        '''
        Constructor
        :param: service Reference to service "interface" that will resolve
            service-specific concerns. A service may be a streaming system
            or local media playback
        :param: Top-level directory to store caching information for this
            music service/playback object type
        '''
        self.service = service
        self.cachePath = cachePath
        # dictionary of playlists; playlist id from service is the key
        self.playlists = self.service.getPlaylists()
        # initialize/use cache info
        init_cache()
        # if no playlists available, we have a problem to report up
        if (len(self.playlists.keys()) < 1):
            raise ServiceException("No Playlists Found")
        # ptr to current playlist (pick the first one by default)
        self.cur_id = 0
        self.cur = self.playlists[self.playlists.keys()[self.cur_id]]
        # music player object for the stream
        self.player = gst.element_factory_make("playbin2", "player")
        # set playback device to bluetooth
        alsa_card = gst.element_factory_make("alsasink", "bluetooth")
        # Notes to self about bluetooth:
        # - config for alsa is set is /etc/asound.conf
        # - confic for bluetooth audio is /etc/bluetooth/audio.conf
        # - bluetooth daemon: /etc/init.d/bluetooth 
        # - also make sure that there are no other connections to the speaker
        alsa_card.set_property("device", "bluetooth")
        self.player.set_property("audio-sink", alsa_card)
        # music player bus to watch for events on
        bus = self.player.get_bus()
        bus.enable_sync_message_emission()
        bus.add_signal_watch()
        bus.connect("message", self.msgEvent)

    def msgEvent(self, bus, message):
        '''
        Handles "message" events from the music player's bus
        :param: bus Player communication bus
        :param: message Message object from bus
        '''
        # if the song ends or encounters an error, try the next song
        if ((message.type == gst.MESSAGE_EOS) or 
                (message.type == gst.MESSAGE_ERROR)):
            self.next()

    def init_cache(self):
        '''
        Initialize and use cache info. There is a cache for each service
            that provides the following:
            - Tracks/builds playlist text-to-speech information
        '''
        srvPath = self.cachePath + self.service.strType + "/")
        if not(os.path.exists(srvPath)):
            os.makedirs(srvPath)
        # generate any missing playlist text-to-speech data
        for pl in self.playlists:
            speakFile = srvPath + pl.name + ".wav"
            if not(os.path.exists(speakFile)):
                # write file to cache
                mkTextSpeech(pl.name, speakFile)
            pl.ttsFile = speakFile

    def play(self):
        '''
        Play the current song and return the stream location
        :return: Stream uri
        '''
        # get location of the stream from the current playlist
        mp3Stream = self.service.getStream(self.cur)
        # set the stream location and begin playing music
        self.player.set_property("uri", mp3Stream)
        self.player.set_state(gst.STATE_PLAYING)
        return mp3Stream

    def pause(self):
        '''
        Pause the current song and return the unique id of the song playing
        :return: Stream uri
        '''
        self.player.set_state(gst.STATE_PAUSED)
        return self.service.getStream(self.cur)

    def playPause(self):
        '''
        Plays/Pauses the song based on the current player state
        :return: Results of play() or pause()
        '''
        if (self.player.get_state()[1] == gst.STATE_PLAYING):
            return self.pause()
        return self.play()
        
    def prev(self):
        '''
        Moves to the previous song (wraps-around) and returns that song
        :return: Results of play() function
        '''
        # halt/remove the current song
        self.player.set_state(gst.STATE_NULL)
        # change song in playlist 
        self.cur.prev()
        return self.play()

    def next(self):
        '''
        Moves to the next song (wraps-around) and returns that song
        :return: Results of play() function
        '''
        # perform similar actions as with prev()
        self.player.set_state(gst.STATE_NULL)
        self.cur.next()
        return self.play()

    def prevPl(self):
        '''
        Moves to the previous Playlist (wraps-around) and returns that song
        :return: Results of play() function
        '''
        # halt/remove the current song
        self.player.set_state(gst.STATE_NULL)
        # change playlist
        if (self.cur_id == 0):
            self.cur_id = len(self.playlists.keys()) - 1
        else:
            self.cur_id -= 1
        self.cur = self.playlists[self.playlists.keys()[self.cur_id]]
        return self.play()

    def nextPl(self):
        '''
        Moves to the next Playlist (wraps-around) and returns that song
        :return: Results of play() function
        '''
        # perform similar actions as with prevPl()
        self.player.set_state(gst.STATE_NULL)
        if (self.cur_id == (len(self.playlists.keys()) - 1 )):
            self.cur_id = 0
        else:
            self.cur_id += 1
        self.cur = self.playlists[self.playlists.keys()[self.cur_id]]
        return self.play()

def main():
    '''
    Main execution point for testing
    '''

if __name__ == '__main__':
    main()
