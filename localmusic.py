#/usr/bin/python
from __future__ import print_function
# Python standard lib imports
import sys
# Local imports
from musicservice import MusicService
from playlist import Playlist
from track import Track

'''
localmusic.py
Python file that manages playing songs on local disk
@author: Schuyler Martin <schuylermartin45@gmail.com>
'''
__author__ = "Schuyler Martin"

class LocalService(MusicService):
    '''
    Music Service class that 
    '''
    def __init__(self):
        '''
        Constructor
        '''
        MusicService.__init__(self, "Local Service")

    def getPlaylists(self):
        '''
        Returns a dictionary of playlists from this service
        :return: Dictionary of playlists ([playlist_id] -> playlist)
        '''
        return None

    def getStream(self, playlist):
        '''
        Retrieves a complete playlist structure from all playlist content
        :param: playlist Reference to Playlist object to use
        :return: Music stream location
        '''
        mp3Stream = ""
        return mp3Stream

def main():
    '''
    Main execution point for testing
    '''

if __name__ == '__main__':
    main()
