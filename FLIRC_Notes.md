# Notes on using FLIRC USB Device

As of writing, this project uses the FLIRC USB IR receiver to interpret signals
from an IR remote. It was suggested online that it was easy to use this device
on your own projects. However the API/SDK links on the official website are all
"under construction" and there is little to no documentation as to how to
programatically control the device. 

In not wanting to spend more money on this project than I have to, I will 
attempt to use this device and document all of my findings in this text file,
hoping that it might help someone else who has made the same mistake as I have.

Of course, knowing my luck, by the time I am done the official SDK will be
released. So take this as what you will.

## Downloading the available software:
1. Go to https://flirc.tv/downloads
2. Click on Linux downloads
3. Accept the terms & conditions check box
4. Download and unzip the "Universal Static Package" zip file
    1. This includes 2 compiled programs: Flirc and flirc_util
        1. flirc_util is compiled for both x64 bit Debian and the ARM version
            of Debian used for the Raspberry Pi.
    2. Flirc is (probably) the GUI setup utility
    3. flirc_util provides extensive tools for interacting with the FLIRC USB
        device, including methods for recording and writing the IR 
        configuration data to the EEPROM on the device. Running ```./flirc_util```
        with no arguments will dump all available commands to the console.

## Running the device:
1. A quick test to see if the device is working properly is to run:
    ```
    ./flirc_util wait
    ```
    1. If you get a ```Warning: cannot open USB device``` error message, try
        running the script with root privleges or copy the provided 
        ```51-flirc.rules``` file into /etc/udev/rules.d/ and then unplug/replug
        the device.
        1. On the Pi, I had to make some additional changes. I had to change
            the file name to ```93-flirc.rules``` as some built-in Raspberry Pi
            udev rules were overriding these new rules. Running 
            ```sudo udevadm``` was enough to restart the udev daemon to pick-up
            on these changes.

## Interpretting Signals as code
Initially I thought I would have to reverse-engineer the USB Bus traffic on the
FLIRC device and develop my own driver for it. But after fiddling around with 
some Linux USB monitoring and debugging tools (namely ```usbmon``` and 
```evtest```) I realized that the Raspberry Pi was already interpretting button-
mappings programmed into the EEPROM of the FLIRC receiver as keyboard input.
With this information, I was able to find a Python library, ```evdev```, for 
interpretting key input specifically from this device and was able to leverage
that to handle input to the Pi.
