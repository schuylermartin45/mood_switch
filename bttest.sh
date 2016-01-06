#!/bin/bash
# Two easy ways to test the bt audio:

bluez-test-audio connect 48:E2:44:F3:E7:07

# Last parameter is the audio file to test with
# mplayer -ao alsa:device=bluetooth local_music/playlist1/00_InTheFlesh.mp3
