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

# constant volume values for audio player
VOLUME_DEFAULT = 1.0
# the speech files are way quieter than the rest of the music
VOLUME_SPEECH = 7.0

def mkTextSpeech(text, fileName):
    '''
    Writes a text-to-speech file
    :param: text Text to synthesize
    :param: fileName File name to write-out to
    '''
    # see espeak man page for more info for args
    subprocess.call(["espeak",
        "-s 120",
        "-a 20",
        "-w" + fileName, text])

class Playback:
    '''
    Class that represents the playback system
    '''
    def __init__(self, service, cachePath):
        '''
        Constructor
        :param: service Reference to service "interface" that will resolve
            service-specific concerns. A service may be a streaming system
            usic service/playback object type
        '''
        self.service = service
        self.cachePath = cachePath
        # tracks if we are playing the TTS playlist file now
        self.pl_TTS = False
        # tracks if we are playing the TTS shuffle commands now
        self.shuffle_TTS = False
        # dictionary of playlists; playlist id from service is the key
        self.playlists = self.service.getPlaylists()
        # initialize/use cache info
        self.init_cache()
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
            # if the TTS file is done playing, play the current song
            if (self.pl_TTS):
                self.pl_TTS = False
                self.play()
            elif (self.shuffle_TTS):
                self.shuffle_TTS = False
                self.play()
            # else advance to the next song
            else:
                self.next()

    def init_cache(self):
        '''
        Initialize and use cache info. There is a cache for each service
            that provides the following:
            - Tracks/builds playlist text-to-speech information
        '''
        # in the cache path, check to see if the shuffle sounds are there
        self.shuffle_Files = {}
        self.shuffle_Files[True] = self.cachePath + "shuffleOn.wav"
        self.shuffle_Files[False] = self.cachePath + "shuffleOff.wav"
        if not(os.path.exists(self.shuffle_Files[True])):
            mkTextSpeech("Setting shuffle on ", self.shuffle_Files[True])
        if not(os.path.exists(self.shuffle_Files[False])):
            mkTextSpeech("Setting shuffle off", self.shuffle_Files[False])
        # for each service
        srvPath = self.cachePath + self.service.strType + "/"
        if not(os.path.exists(srvPath)):
            os.makedirs(srvPath)
        # generate any missing playlist text-to-speech data
        for ids, pl in self.playlists.iteritems():
            speakFile = srvPath + pl.name + ".wav"
            if not(os.path.exists(speakFile)):
                # write file to cache
                mkTextSpeech("Playing: " + pl.name + ".", speakFile)
            pl.ttsFile = "file://" + speakFile

    def play(self):
        '''
        Play the current song and return the stream location
        :return: Stream uri
        '''
        pl = self.playlists[self.playlists.keys()[self.cur_id]]
        # special case for playing the text-to-speech message
        if ((self.pl_TTS) and (pl.ttsFile != None)):
            self.player.set_property("volume", VOLUME_SPEECH)
            mp3Stream = pl.ttsFile
        else:
            self.player.set_property("volume", VOLUME_DEFAULT)
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

    def shuffle(self):
        '''
        Shuffles/deshuffles every playlist (keeps a consistent state across all
        '''
        shuffle_TTS = True
        # play appropriate sound notification
        ttsFile = "file://" + self.shuffle_Files[not(self.cur.isShuffle)]
        self.player.set_property("volume", VOLUME_SPEECH)
        # all playlists should have the same shuffle state
        for ids, pl in self.playlists.iteritems():
            pl.shuffle()
        # play audio clip messaging
        self.player.set_state(gst.STATE_NULL)
        self.player.set_property("uri", ttsFile)
        self.player.set_state(gst.STATE_PLAYING)

    def prevPl(self):
        '''
        Moves to the previous Playlist (wraps-around) and returns that song
        :return: Results of play() function
        '''
        # attempt to play the identifying playlist name
        self.pl_TTS = True
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
        self.pl_TTS = True
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
