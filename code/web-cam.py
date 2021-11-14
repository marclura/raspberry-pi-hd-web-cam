#!/bin/python

import picamera
import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)  # set up GPIO numbering

GPIO.setup(17, GPIO.IN) # rotate
GPIO.setup(27, GPIO.IN) # power off
GPIO.setup(22, GPIO.OUT) # led

camera = picamera.PiCamera()

# variables
old_btn_rotate = 0
rotation = 0    # rotation type, from 0 to 3, see rotate()
power_off_count = 0 # times to count to power off

# Start the camera live preview on the HDMI
camera.start_preview()
GPIO.output(22, 1)      # LED on

def rotate():
        if rotation == 0:
                camera.hflip = False
                camera.vflip = False
        elif rotation == 1:
                camera.vflip = True
        elif rotation == 2:
                camera.hflip = True
        elif rotation == 3:
                camera.vflip = False

try:
        while True:
                # Rotation button
                if GPIO.input(17) == 1 and  old_btn_rotate == 0:
                        # print( "Rotate pressed")
                        old_btn_rotate = 1
                        # camera.vflip = True
                        if rotation <= 2:
                                rotation += 1
                        else:
                                rotation = 0
                        rotate()
                elif GPIO.input(17) == 0 and old_btn_rotate == 1:
                        old_btn_rotate = 0
                        # camera.vflip = False
                        # print("Rotate released")

                # Stop button
                if GPIO.input(27) == 1:
                        power_off_count += 1

                        if power_off_count >= 20:
                                GPIO.output(22, 0) # switch off the LED
                                print("Power off")
                                os.system("sudo poweroff") # send system command to power off

                time.sleep(0.1)
finally:
        GPIO.cleanup()
