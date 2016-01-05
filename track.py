#/usr/bin/python
from __future__ import print_function

'''
track.py
Python class that represents a single track/song
@author: Schuyler Martin <schuylermartin45@gmail.com>
'''
__author__ = "Schuyler Martin"

class Track:
    '''
    Class that represents a track/song to be played by the Pi
    '''
    def __init__(self, id, name):
        '''
        Constructor
        :param: id Track unique id (unique to streaming service or playlist)
        :param: name Name of the track
        '''
        self.id = id
        self.name = name

def main():
    '''
    Main execution point for testing
    '''

if __name__ == '__main__':
    main()
