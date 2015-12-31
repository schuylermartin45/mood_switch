#/usr/bin/python
from __future__ import print_function

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

    def current(self):
        '''
        Gets the unique id of the current song playing
        '''
        return tracks[self.cur]['id']

    def prev(self):
        '''
        Moves to the previous song (wraps-around) and returns that song
        '''
        if (self.cur == 0):
            self.cur = len(self.tracks) - 1
        else:
            self.cur -= 1
        return current(self)

    def next(self):
        '''
        Moves to the next song (wraps-around) and returns that song
        '''
        if (self.cur == (len(self.tracks) - 1)):
            self.cur = 0
        else:
            self.cur += 1
        return current(self)

def main():
    '''
    Main execution point for testing
    '''

if __name__ == '__main__':
    main()
