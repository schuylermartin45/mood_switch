#/usr/bin/python
from __future__ import print_function
import random
import copy
'''
playlist.py
Python class that represents a playlist
@author: Schuyler Martin <schuylermartin45@gmail.com>
'''
__author__ = "Schuyler Martin"

class Playlist:
    '''
    Class that represents a playlist to be played by the Pi
    '''
    def __init__(self, id, name, tracks):
        '''
        Constructor
        :param: id Playlist unique id (unique to streaming service)
        :param: name Name of the playlist
        :param: tracks List of track objects
        '''
        self.id = id
        self.name = name
        # keep two copies of the tracks (used for suffling)
        self.tracks_original = copy.deepcopy(tracks)
        self.tracks_shuffle = copy.deepcopy(tracks)
        self.isShuffle = False
        # default to pointing to the original
        self.tracks = self.tracks_original
        # current track
        self.cur = 0
        # file that stores the text-to-speech read-out of the file (to be set
        # by the playback service)
        self.ttsFile = None

    def __str__(self):
        '''
        __str__
        :return: String representation of a Playlist
        '''
        trackStr = ""
        for track in self.tracks:
            trackStr += str(track) + ", "
        return str(self.id) + ": " + self.name + " -> [ " + trackStr + " ]"

    def current(self):
        '''
        Return the unique id of the current song (to play)
        :return: Unique id of the song to play
        '''
        song_id = self.tracks[self.cur].id
        return song_id

    def prev(self):
        '''
        Moves to the previous song (wraps-around) and returns that song
        :return: Unique id of the song to play
        '''
        if (self.cur == 0):
            self.cur = len(self.tracks) - 1
        else:
            self.cur -= 1
        return self.current()

    def next(self):
        '''
        Moves to the next song (wraps-around) and returns that song
        :return: Unique id of the song to play
        '''
        if (self.cur == (len(self.tracks) - 1)):
            self.cur = 0
        else:
            self.cur += 1
        return self.current()

    def shuffle(self):
        '''
        Shuffles/de-shuffles a playlist
        :return: Unique id of the song to play
        '''
        self.isShuffle = not(self.isShuffle)
        if (self.isShuffle):
            random.shuffle(self.tracks_shuffle)
            self.tracks = self.tracks_shuffle
        else:
            self.tracks = self.tracks_original

def main():
    '''
    Main execution point for testing
    '''

if __name__ == '__main__':
    main()
