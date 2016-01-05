#/usr/bin/python
from __future__ import print_function
import pygst
import gst

'''
playback.py
Python class that controls playback
    Uses GStreamer w/ Python Bindings (gstreamer.freedesktop.org)
@author: Schuyler Martin <schuylermartin45@gmail.com>
'''
__author__ = "Schuyler Martin"

class Playlist:
    '''
    Class that represents the playback system
    '''
    def __init__(self, service):
        '''
        Constructor
        :param: service Reference to service "interface" that will resolve
            service-specific concerns. A service may be a streaming system
            or local media playback
        '''
        # dictionary of playlists; playlist id from service is the key
        self.playlists = service.getPlaylists()
        # ptr to current playlist (pick the first one by default)
        self.cur = playlists[self.playlists.keys()[0]]
        # music player object for the stream
        self.player = gst.element_factory_make("playbin", "player")

    def play(self):
        '''
        Play the current song and return the unique id of the song playing
        '''
        # halt any previously playing song
        if (self.player.get_state() != gst.STATE_NULL):
            self.player.set_state(gst.STATE_NULL)
        # get location of the stream from the current playlist
        mp3Stream = self.service.getStream(self.cur)
        # set the stream location and begin playing music
        self.player.set_property("uri", mp3Stream)
        self.player.set_state(gst.STATE_PLAYING)
        return song_id

    def pause(self):
        '''
        Pause the current song and return the unique id of the song playing
        '''
        self.player.set_state(gst.STATE_PAUSED)
        return self.tracks[self.cur]['id']
        
    def prev(self):
        '''
        Moves to the previous song (wraps-around) and returns that song
        '''
        return self.play()

    def next(self):
        '''
        Moves to the next song (wraps-around) and returns that song
        '''
        return self.play()

def main():
    '''
    Main execution point for testing
    '''

if __name__ == '__main__':
    main()
