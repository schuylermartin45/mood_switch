#/usr/bin/python
from __future__ import print_function

'''
musicservice.py
Parent class for all music services. "Enforces" a strict interface
@author: Schuyler Martin <schuylermartin45@gmail.com>
'''
__author__ = "Schuyler Martin"

class MusicService:
    '''
    Music Service class "enforces" a common interface for all music services
    '''
    def __init__(self, strType):
        '''
        Constructor
        :param: strType String version of the service type's name
        '''
        self.strType = strType

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
        Retrieves a complete playlist structure from all playlist content
        :param: playlist Reference to Playlist object to use
        :return: Music stream location
        '''
        # "Enforce" interface
        raise Exception("getStream() not implemented for service " 
            + self.strType)

def main():
    '''
    Main execution point for testing
    '''

if __name__ == '__main__':
    main()
