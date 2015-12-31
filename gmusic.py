#/usr/bin/python
from __future__ import print_function
# import unofficial Google Music API by GitHub user: simon-weber
from gmusicapi import Mobileclient
# Python standard lib imports
import sys

'''
gmusic.py

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

def init(fileName):
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
    logged_in = api.login(user, app_pwd, Mobileclient.FROM_MAC_ADDRESS)
    # error handling for auth
    if not(logged_in):
        print("ERROR: Unable to log in.", file=sys.stderr)
        exit(1)
    return api

def main():
    '''
    Main execution point to test the streaming service
    '''
    api = init(DEFAULT_AUTH)

if __name__ == '__main__':
    main()
