#/usr/bin/python
from __future__ import print_function
import threading
import time
# RPi control
import RPi.GPIO as GPIO

'''
servocontrol.py
Python module that handles the motor control for the mood switch project
@author: Schuyler Martin <schuylermartin45@gmail.com>
'''
__author__ = "Schuyler Martin"

# Physical pin numbering
SIGNAL_PIN = 8

class Switch():
    '''
    Class for motorized switch
    '''
    def __init__(self):
        '''
        Constructor
        '''
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(SIGNAL_PIN, GPIO.OUT)
        # set pin up for PWM
        self.pin = GPIO.PWM(SIGNAL_PIN, 50)
        self.pin.start(7.5)
        self.center()
        # boolean control for on/off switch. Assume light is on.
        self.isOn = True

    def left(self):
        '''
        Turn servo to the left (0 degrees)
        '''
        self.pin.ChangeDutyCycle(12.5)
        time.sleep(1)

    def center(self):
        '''
        Turn servo to the center (90 degrees)
        '''
        self.pin.ChangeDutyCycle(7.5)
        time.sleep(1)

    def right(self):
        '''
        Turn servo to the right (180 degrees)
        '''
        self.pin.ChangeDutyCycle(2.5)
        time.sleep(1)
    
    def turnOn(self):
        '''
        Turn the light on
        Pre/Post: Servo is in center state
        '''
        self.left()
        self.center()
        self.isOn = True

    def turnOff(self):
        '''
        Turn the light off
        Pre/Post: Servo is in center state
        '''
        self.right()
        self.center()
        self.isOn = False

    def turnSwitch(self):
        '''
        Flip the switch based on known state
        '''
        if (self.isOn):
            self.turnOff()
        else:
            self.turnOn()

    def __del__(self):
        '''
        Destructor (cleans-up messaging to GPIO)
        '''
        self.pin.stop()
        GPIO.cleanup()

def main():
    '''
    Main execution point for testing
    '''
    servo = Switch()

    try:
        while(True):
            keyIn = raw_input("Turn: ")
            servo.turnSwitch()

    except KeyboardInterrupt:
        exit(0)

if __name__ == '__main__':
    main()
