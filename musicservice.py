#/usr/bin/python
from __future__ import print_function

'''
musicservice.py
Parent class for all music services. "Enforces" a strict interface.
These classes are used by the Playback class.
@author: Schuyler Martin <schuylermartin45@gmail.com>
'''
__author__ = "Schuyler Martin"

class MusicService:
    '''
    Music Service class "enforces" a common interface for all music services
    '''
    def __init__(self, strType, plTypeTTS):
        '''
        Constructor
        :param: strType String version of the service type's name
        :param: plTypeTTS String indicating what the playlist is over TTS
            (For example, radio stations may report "Playing station x" over
            "Playing playlist x")
        '''
        self.strType = strType
        self.plTypeTTS = plTypeTTS

    def __str__(self):
        '''
        __str__()
        :return: Return the service's string-name equivalent
        '''
        return self.strType

    def getPlaylists(self):
        '''
        Returns a dictionary of playlists from this service
        :return: Dictionary of playlists ([playlist_id] -> playlist)
        '''
        # "Enforce" interface
        raise Exception("getPlaylists() not implemented for service " 
            + self.strType)

    def getStream(self, playlist):
        '''
        Retrieves the location of the (current) song to play
        :param: playlist Reference to Playlist object to use
        :return: Music stream location
        '''
        # "Enforce" interface
        raise Exception("getStream() not implemented for service " 
            + self.strType)

class ServiceException(Exception):
    '''
    Custom exception to throw if there is an issue with a music service
    '''
    pass

def main():
    '''
    Main execution point for testing
    '''

if __name__ == '__main__':
    main()
