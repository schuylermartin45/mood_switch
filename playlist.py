#/usr/bin/python
from __future__ import print_function
import pygst
import gst

'''
playlist.py
Python class that represents a playlist and controls playback
    Uses GStreamer w/ Python Bindings (gstreamer.freedesktop.org)
@author: Schuyler Martin <schuylermartin45@gmail.com>
'''
__author__ = "Schuyler Martin"

class Playlist:
    '''
    Class that represents a playlist to be played by the Pi
    '''
    def __init__(self, jdict):
        '''
        Constructor
        :param: JSON object that contains all the playlist info from Google
        '''
        # === Google data, so we track all of it if need be ===
        self.data = jdict
        # === Aliases for commonly needed values, for convience ===
        self.id = jdict['id']
        self.name = jdict['name']
        self.tracks = jdict['tracks']
        # === New info want to track ===
        # current track
        self.cur = 0
        # music player object for the stream
        self.player = get.element_factory_make("playbin", "player")

    def play(self):
        '''
        Play the current song and return the unique id of the song playing
        '''
        song_id = tracks[self.cur]['id']
        # halt any previously playing song
        if (player.get_state() != gst.STATE_NULL):
            player.set_state(gst.STATE_NULL)
        # according to the API, these URLs expire so unfortunately we can't
        # cache/store them somewhere
        mp3Stream = Mobileclient.get_stream_url(song_id)
        # set the stream location and begin playing music
        player.set_property("uri", mp3Stream)
        player.set_state(gst.STATE_PLAYING)
        return song_id

    def pause(self):
        '''
        Pause the current song and return the unique id of the song playing
        '''
        player.set_state(gst.STATE_PAUSED)
        return tracks[self.cur]['id']
        
    def prev(self):
        '''
        Moves to the previous song (wraps-around) and returns that song
        '''
        if (self.cur == 0):
            self.cur = len(self.tracks) - 1
        else:
            self.cur -= 1
        return play(self)

    def next(self):
        '''
        Moves to the next song (wraps-around) and returns that song
        '''
        if (self.cur == (len(self.tracks) - 1)):
            self.cur = 0
        else:
            self.cur += 1
        return play(self)

def main():
    '''
    Main execution point for testing
    '''

if __name__ == '__main__':
    main()
