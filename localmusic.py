#/usr/bin/python
from __future__ import print_function
# Python standard lib imports
import os
from os.path import *
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

# Tuple of file types that GStreamer can play (that I know of thus far)
FILE_TYPES = ('.mp3', '.ogg')

class LocalService(MusicService):
    '''
    Music Service class that 
    '''
    def __init__(self, path):
        '''
        Constructor
        :param: path Path to directory storing local music
            Local music is stored in the following format:
                [Top Level Path]
                |-- Playlist 0
                    |-- Song 0
                    |-- Song 1
                |-- Playlist 1
                    |-- Song 0
                etc...
        '''
        MusicService.__init__(self, "Local Service")
        self.path = path
        self.playlists = {}
        # dictionary (acting like a multi-dimensional array) that stores 
        # locations of song files per playlist 
        # (i.e. streams[playlist_id,song_id])
        self.streams = {}
        pl_id = 0
        for dir in os.listdir(self.path):
            # directories indicate playlists
            pl_path = os.path.join(self.path, dir)
            if (os.path.isdir(pl_path)):
                track_id = 0
                tracks = []
                for track in os.listdir(pl_path):
                    # tracks are files in a directory
                    track_path = os.path.join(pl_path, track)
                    # TODO: Filter for music files only
                    if ((os.path.isfile(track_path)) and 
                            (track_path.endswith(FILE_TYPES))):
                        tracks.append(Track(track_id, track))
                        stream_uri = "file:/" + os.path.abspath(track_path)
                        self.streams[pl_id,track_id] = stream_uri 
                        track_id += 1
                # construct final playlist
                self.playlists[pl_id] = Playlist(pl_id, dir, tracks)
                pl_id += 1
                

    def getPlaylists(self):
        '''
        Returns a dictionary of playlists from this service
        :return: Dictionary of playlists ([playlist_id] -> playlist)
        '''
        return self.playlists

    def getStream(self, playlist):
        '''
        Retrieves the location of the (current) song to play
        :param: playlist Reference to Playlist object to use
        :return: Music stream location
        '''
        return self.streams[playlist.id,playlist.current()]

def main():
    '''
    Main execution point for testing
    '''
    testService = LocalService("local_music")
    for key in testService.getPlaylists().keys():
        print("Playlist: ")
        print(testService.getPlaylists()[key])
    print(testService.streams)

if __name__ == '__main__':
    main()
