#/usr/bin/python
from __future__ import print_function
from musicservice import MusicService
from playlist import Playlist
from track import Track
'''
radioservice.py
Music service for online radio stations.
@author: Schuyler Martin <schuylermartin45@gmail.com>
'''
__author__ = "Schuyler Martin"

# dictionary of known stations
STATION_DICT = {
    'Ambient noise test' : "http://radio.hbr1.com:19800/ambient.ogg",
    'Russian Revolution Radio' : "http://revolutionradio.ru/live.ogg",
    'Radio Rock 1' : "http://stream.radioreklama.bg:80/radio1rock.ogg",
    'WPCE The Classical Station' : "http://audio-ogg.ibiblio.org:8000/wpce.ogg",
    'UK Absolute Classic Rock' : "http://icecast.timlradio.co.uk:80/absoluteradio.co.uk/acflac.ogg",
    'UK Sixties Radio' : "http://icecast.timlradio.co.uk:80/absoluteradio.co.uk/a6flac.ogg",
    'UK Seventies Radio' : "http://icecast.timlradio.co.uk:80/absoluteradio.co.uk/a7flac.ogg",
    'UK Eighties Radio' : "http://icecast.timlradio.co.uk:80/absoluteradio.co.uk/a8flac.ogg",
    'Hungarian Jazz Radio' : "http://194.38.105.41:8000/jazzradio_192.ogg",
}

class RadioService(MusicService):
    '''
    Music Service that handles online radio stations
        Note that in this case, a "playlist" is a single radio station/stream
    '''
    def __init__(self):
        '''
        Constructor
        '''
        MusicService.__init__(self, "Radio Service", "station")
        self.stations = {}
        id = 0
        for name, url in STATION_DICT.iteritems():
            # there is only one track per stations; the main url
            tracks = [Track(0, name)]
            self.stations[id] = Playlist(id, name, tracks)
            id += 1

    def getPlaylists(self):
        '''
        Returns a dictionary of playlists from this service
        :return: Dictionary of playlists ([playlist_id] -> playlist)
        '''
        return self.stations

    def getStream(self, playlist):
        '''
        Retrieves the location of the (current) song to play
        :param: playlist Reference to Playlist object to use
        :return: Music stream location
        '''
        return STATION_DICT[playlist.name]

def main():
    '''
    Main execution point for testing
    '''

if __name__ == '__main__':
    main()
