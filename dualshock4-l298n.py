#!/usr/bin/env python
# coding: Latin-1

# Load library functions we want
import time
import os
import sys
import pygame
from gpiozero import OutputDevice # use gpiozero module to handle L298N input/output

# initialize L298N for 2 wheel robot *********************start****************
ENA = OutputDevice(5)
ENB = OutputDevice(6)

# control left wheel -- OUT1 & OUT2 for left wheel
IN1 = OutputDevice(12)
IN2 = OutputDevice(16)

# control right wheel -- OUT3 & OUT4 for right wheel
IN3 = OutputDevice(20)
IN4 = OutputDevice(21)

# initialize L298N for 2 wheel robot *******************end********************

global joystick
# Settings for the joystick
axisR2 = 4                          # Joystick axis to read for up / down position
axisL2= 6
axisUpDownInverted = True               # Set this to True if up and down appear to be swapped
axisLeftRight = 0                       # Joystick axis to read for left / right position
axisLeftRightInverted = True            # Set this to True if left and right appear to be swapped
buttonResetEpo = 3                      # Joystick button number to perform an EPO reset (Start)
buttonSlow = 6                          # Joystick button number for driving slowly whilst held (L2)
slowFactor = 0.5                        # Speed to slow to when the drive slowly button is held, e.g. 0.5 would be half speed
buttonFastTurn = 9                      # Joystick button number for turning fast (R2)
interval = 0.00                         # Time between updates in seconds, smaller responds faster but uses more processor time
TURN_MULTIPLIER = 0.4
# Power settings
voltageIn = 8.4                         # Total battery voltage to the ZeroBorg (change to 9V if using a non-rechargeable battery)
voltageOut = 6.0                        # Maximum motor voltage

# Setup the power limits
if voltageOut > voltageIn:
    maxPower = 1.0
else:
   # maxPower = voltageOut / float(voltageIn)
    maxPower = 2.0


def Dualshock4Init():

    global joystick
    # Setup pygame and wait for the joystick to become available
    #os.environ["SDL_VIDEODRIVER"] = "dummy" # Removes the need to have a GUI window
    pygame.init()

    print 'Waiting for joystick... (press CTRL+C to abort)'

    while True:
        try:
            try:
                pygame.joystick.init()
                # Attempt to setup the joystick
                if pygame.joystick.get_count() < 1:
                    # No joystick attached, toggle the LED
                    pygame.joystick.quit()
                    time.sleep(0.1)
                else:
                    # We have a joystick, attempt to initialise it!
                    joystick = pygame.joystick.Joystick(0)
                    break
            except pygame.error:
                # Failed to connect to the joystick, toggle the LED
                pygame.joystick.quit()
                time.sleep(0.1)
        except KeyboardInterrupt:
            # CTRL+C exit, give up
            print '\nUser aborted'
            sys.exit()
    print 'Joystick found'
    joystick.init()

def robotControl():
    global joystick
    try:
        print 'Press CTRL+C to quit'
        driveLeft = 0.0
        driveRight = 0.0
        running = True
        hadEvent = False
        upDown = 0.0
        leftRight = 0.0
        # Loop indefinitely
        while running:
            # Get the latest events from the system
            hadEvent = False
            events = pygame.event.get()
            # Handle each event individually
            for event in events:
                print("event:{}".format(event.type))
                if event.type == pygame.QUIT:
                    # User exit
                    running = False
                elif event.type == pygame.JOYBUTTONDOWN:
                    # A button on the joystick just got pushed down
                    hadEvent = True
                elif event.type == pygame.JOYAXISMOTION:
                    # A joystick has been moved
                    hadEvent = True
                if hadEvent:
                    # Read axis positions (-1 to +1)
                    if axisUpDownInverted:
                        upDown = -joystick.get_axis(axisR2)  # release --> 1     half 0     full press --> -1
                        throttle = upDown - 1
                        if throttle < -1.0:
                            throttle = -1.0
                        print("throttle : {0} ".format(throttle))
                    else:
                        upDown = joystick.get_axis(axisR2)
                    if axisLeftRightInverted:
                        leftRight = -joystick.get_axis(axisLeftRight)
                        print("leftRight : {}".format(leftRight))
                    else:
                        leftRight = joystick.get_axis(axisLeftRight)
                    # Apply steering speeds
                    if not joystick.get_button(buttonFastTurn):
                        leftRight *= 1

                    # Determine the drive power levels
                    if joystick.get_button(axisL2): # to REVERSE the car
                        driveLeft = throttle
                        driveRight = throttle
                    else:                                   # to move FORWARD
                        driveLeft = -throttle
                        driveRight = -throttle

                    if leftRight < -0.05:
                        # Turning right
                        IN1.on()
                        IN2.off()
                        IN3.off()
                        IN4.on()

                        driveLeft = driveLeft*( 1.0 - (1.0 * leftRight))
                        driveRight = driveRight - driveLeft*TURN_MULTIPLIER
                    elif leftRight > 0.05:
                        # Turning left

                        IN1.off()
                        IN2.on()
                        IN3.on()
                        IN4.off()

                        driveRight= driveRight*( 1.0 + (1.0 * leftRight))
                        driveLeft= driveLeft - driveRight*TURN_MULTIPLIER
                    print("driveL :{0:.2f} || driveR : {1:.2f} ".format(driveLeft,driveRight))


                    # Set the motors to the new speeds
                    ENA.value = driveLeft
                    ENB.value = driveRight

            # Wait for the interval period
            time.sleep(interval) # default = 0

    except KeyboardInterrupt:
        # CTRL+C exit, disable all drives
        print('shutting down...')
    print

if __name__=="__main__":
    Dualshock4Init()
    robotControl()
