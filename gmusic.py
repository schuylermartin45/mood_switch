#/usr/bin/python
from __future__ import print_function
# import unofficial Google Music API by GitHub user: simon-weber
from gmusicapi import Mobileclient
from gmusicapi import Webclient
# Python standard lib imports
import sys
import json
# Local imports
from musicservice import MusicService

# TODO This is very broken right now and does not conform to the new standards.
# Will get back to later(?)

'''
gmusic.py
Python file that handles interactions between Google Music via the un-official
    API developed by GitHub user simon-weber
    See more at: github.com/simon-weber/gmusicapi
@author: Schuyler Martin <schuylermartin45@gmail.com>
'''
__author__ = "Schuyler Martin"

# Default authentication file name
# Format of the file is simple:
# 1st line: User name
# 2nd line: Password*
# * It should be noted that I've chosen to generate app-specific passwords from
#   Google since that seems to be more secure and allows me to get around the
#   lack of 2-factor auth in this API
DEFAULT_AUTH = "auth.file"

# ID of a test playlist
DEBUG_PL1 = "07969458-13bb-4fe5-a9d4-c1122a4fe5bb" # "Girl"

def printJson(jstr):
    '''
    Pretty prints json string (for debugging purposes)
    :param: str JSON string to pretty print
    '''
    print(json.dumps(jstr, sort_keys=True, indent=4, separators=(',', ': ')))

class GMusicService(MusicService):
    '''
    Music Service for the Google Music API
    '''

    def __init__(self, fileName):
        '''
        Initializes the API with user credentials
        :param: fileName Reference to the file with authentication information
        :return: Reference to the API
        '''
        api = Mobileclient()
        # read in the auth file
        cntr = 0
        for line in open(fileName):
            if (cntr == 0):
                user = line.strip()
            if (cntr == 1):
                app_pwd = line.strip()
            cntr += 1
        # bail before potential exception
        if (cntr != 2):
            print("ERROR: Improperly formatted auth file.", file=sys.stderr)
            exit(1)
        # TODO improve MAC id
        logged_in = api.login(user, app_pwd, Mobileclient.FROM_MAC_ADDRESS)
        # error handling for auth
        if not(logged_in):
            print("ERROR: Unable to log in.", file=sys.stderr)
            exit(1)
        return api

    def getPlaylists(self, allContent, id):
        '''
        Retrieves a complete playlist structure from all playlist content
        :param: allContent JSON object of all playlists and contents of all lists
        :param: id Playlist unique id
        :return: Playlist content of interest or None if no match
        '''
        # iterate over list and check for a match
        for pl in allContent:
            if (pl['id'] == id):
                return pl
        # TODO handle this better(?)
        return None

def main():
    '''
    Main execution point to test the streaming service
    '''
    #api = init(DEFAULT_AUTH)
    # the API doesn't provide a way to get the contents of just one playlist
    # so you are forced to get all playlists and songs in the playlist at once
    #allContent = json.loads(json.dumps(api.get_all_user_playlist_contents()))
    #playlist = Playlist(api, getPlaylist(allContent, DEBUG_PL1))
    #print("Attempting to play")
    #playlist.play()
    #print("Spinlock")
    #while(True):
    #    pass

if __name__ == '__main__':
    main()
