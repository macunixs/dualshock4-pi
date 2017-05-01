# dualshock4-pi
Procedures to install driver for Dualshock 4 on Raspberry Pi 3

Copy and paste all these commands to complete the installation.
Make sure the Dualshock 4 controller is charged to ensure reliable connection later on.

Commands list:

<code>sudo apt-get update</code>

sudo apt install python-dev python3-dev python-pip python3-pip

<b>Install for Python 3</b>:
sudo pip3 install ds4drv

<b>Install for Python 2</b>:
sudo pip install ds4drv

<b>Allow non-root users to control the ds4drv joystick:</b>

sudo wget https://raw.githubusercontent.com/chrippa/ds4drv/master/udev/50-ds4drv.rules -O /etc/udev/rules.d/50-ds4drv.rules

sudo udevadm control --reload-rules

sudo udevadm trigger


<h3>By now, the driver has been fully installed and you can try to perform pairing with Dualshock 4</h3>

<h3>Make sure Bluetooth on the Pi is turned ON. Then, press and hold (PS button) + (Share button) on Dualshock 4
Hold until the LED on the controller blinks rapidly</h3>

<b>On the terminal run this command:</b>

sudo ds4drv

<b>If everything is correct, the Pi will detect the controller.</b>

<b>*************************************************************************************************</b>

<b>Now configure ds4drv to run at startup by editing the rc.local file:</b>

sudo nano /etc/rc.local

<b>After the # By default this script does nothing. line, add a new line with the contents:</b>

/usr/local/bin/ds4drv &

<b>Now just reboot the Pi so that the driver will be started at boot.</b>

<b>Once rebooted, enter this command to check if ds4drv driver is running in the background as root</b>

<code>ps aux | grep python</code>
