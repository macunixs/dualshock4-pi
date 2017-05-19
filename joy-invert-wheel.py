#!/usr/bin/env python
# coding: Latin-1

# Load library functions we want
import time
import os
import sys
import pygame
import ZeroBorg


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

def ZeroBorgInit():
    global ZB
    # Re-direct our output to standard error, we need to ignore standard out to hide some nasty print statements from pygame
    sys.stdout = sys.stderr

    # Setup the ZeroBorg
    ZB = ZeroBorg.ZeroBorg()
    #ZB.i2cAddress = 0x44                  # Uncomment and change the value if you have changed the board address
    ZB.Init()
    if not ZB.foundChip:
        boards = ZeroBorg.ScanForZeroBorg()
        if len(boards) == 0:
            print 'No ZeroBorg found, check you are attached :)'
        else:
            print 'No ZeroBorg at address %02X, but we did find boards:' % (ZB.i2cAddress)
            for board in boards:
                print '    %02X (%d)' % (board, board)
            print 'If you need to change the I�C address change the setup line so it is correct, e.g.'
            print 'ZB.i2cAddress = 0x%02X' % (boards[0])
        sys.exit()
    #ZB.SetEpoIgnore(True)                 # Uncomment to disable EPO latch, needed if you do not have a switch / jumper
    # Ensure the communications failsafe has been enabled!
    failsafe = False
    for i in range(5):
        ZB.SetCommsFailsafe(True)
        failsafe = ZB.GetCommsFailsafe()
        if failsafe:
            break
    if not failsafe:

        print 'Board %02X failed to report in failsafe mode!' % (ZB.i2cAddress)
        sys.exit()
    ZB.ResetEpo()




def Dualshock4Init():
    global ZB
    global joystick
    # Setup pygame and wait for the joystick to become available
    ZB.MotorsOff()
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
                    ZB.SetLed(not ZB.GetLed())
                    pygame.joystick.quit()
                    time.sleep(0.1)
                else:
                    # We have a joystick, attempt to initialise it!
                    joystick = pygame.joystick.Joystick(0)
                    break
            except pygame.error:
                # Failed to connect to the joystick, toggle the LED
                ZB.SetLed(not ZB.GetLed())
                pygame.joystick.quit()
                time.sleep(0.1)
        except KeyboardInterrupt:
            # CTRL+C exit, give up
            print '\nUser aborted'
            ZB.SetLed(True)
            sys.exit()
    print 'Joystick found'
    joystick.init()
    ZB.SetLed(False)

def robotControl():
    global ZB
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
                        driveLeft = -throttle
                        driveRight = -throttle
                    else:                                   # to move FORWARD
                        driveLeft = throttle
                        driveRight = throttle
                        
                    if leftRight < -0.05:
                        # Turning kanan
                        driveLeft = driveLeft*( 1.0 - (1.0 * leftRight))
                        driveRight = driveRight - driveLeft*TURN_MULTIPLIER
                    elif leftRight > 0.05:
                        # Turning left 
                        driveRight= driveRight*( 1.0 + (1.0 * leftRight))
                        driveLeft= driveLeft - driveRight*TURN_MULTIPLIER
                    print("driveL :{0:.2f} \/ driveR : {1:.2f} ".format(driveLeft,driveRight))

                    # Check for button presses
                    if joystick.get_button(buttonResetEpo):
                        ZB.ResetEpo()
                    # Set the motors to the new speeds
                    ZB.SetMotor1(driveLeft * maxPower)
                    ZB.SetMotor3(driveRight * maxPower)
               
            # Change the LED to reflect the status of the EPO latch
            ZB.SetLed(ZB.GetEpo())
            # Wait for the interval period
            time.sleep(interval)
        # Disable all drives
        ZB.MotorsOff()
    except KeyboardInterrupt:
        # CTRL+C exit, disable all drives
        ZB.MotorsOff()
    print

if __name__=="__main__":
    ZeroBorgInit()
    Dualshock4Init()
    robotControl()
