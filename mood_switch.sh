#!/bin/bash
# Script that starts the mood_switch app
# We want to wrap this command in a batch script for a few reasons:
# - Makes the daemon code look a bit cleaner
# - Allows the daemon script to able to kill the app safely (The alternative 
#   way would call for killing all 'python' processes which is a bad idea)
# - Allows us to enforce only one running instance of the program



MOOD_SW_PATH="/home/pi/projects/mood_switch/remote.py"

BT_ERROR_CODE="22"

function rerun {
    python ${MOOD_SW_PATH}
    # restart the app after Bluetooth has disconnected
    # (For some weird reason the Pi wasn't registering the bluetooth service
    # correctly with the dbus service and thus we could only get a disconnect
    # once and could not poll for it again...and it was difficult finding
    # any documentation as to how to clean-up the gstreamer music pipeline
    if [ "$?" = "22" ]; then
        rerun
    fi
}

MS_CHK_PID=$(pgrep mood_switch.sh)
# prevent multiple running instances by checking pgrep against this instance's
# PID value (which is stored in the bash variable $$)
if [ "$$" = "${MS_CHK_PID}" ]; then
    rerun
fi
