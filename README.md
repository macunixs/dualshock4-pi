# DUALSHOCK 4 + Raspberry Pi 3

<b>This is just a simplified compilation of commands needed to get the Dualshock 4 up and running on the Raspberry Pi 3.</b>

Credit to these links/websites for the guidance:

https://github.com/retropie/retropie-setup/wiki/PS4-Controller

https://github.com/chrippa/ds4drv

https://www.piborg.org/joyborg

<h1>Procedures to install linux driver for Dualshock 4 on Raspberry Pi 3</h1>

<b>Copy</b> and <b>paste</b> all these commands to complete the installation.
Make sure the Dualshock 4 controller is charged to ensure reliable bluetooth connection later on.

<b>Commands list:</b>

<h2>Step 0:</h2> 

<code>sudo apt-get update</code>

<h2>Step 1:</h2> 

You will now need to run the following to ensure the generic joystick drivers are installed first:

<code>sudo apt-get -y install joystick</code>

<h2>Step 2:</h2> 

Then you will want to run jstest as follows:

<code>jstest /dev/input/js0</code>

<b>Note: If you run the above command <code>jstest</code> for the first time, you will get this error: <code>jstest: No such file or directory</code> It is because there is no Joystick connected yet. Don't worry. Just proceed to Step 3.</b>

<h2>Step 3:</h2> 

<code>sudo apt install python-dev python3-dev python-pip python3-pip</code>

<h2>Step 4:</h2> 

<i>(install either one or both)</i> 

<b>Install for Python 3</b>:
<code>sudo pip3 install ds4drv</code>

<b>Install for Python 2</b>:
<code>sudo pip install ds4drv</code>

<h2>Step 5:</h2>  

<b>Allow non-root users to control the ds4drv joystick: Location:<code>/etc/udev/rules.d/</code></b>

<code>sudo wget https://raw.githubusercontent.com/chrippa/ds4drv/master/udev/50-ds4drv.rules -O /etc/udev/rules.d/50-ds4drv.rules</code>

<code>sudo udevadm control --reload-rules</code>

<code>sudo udevadm trigger</code>


<h4>By now, the driver is fully installed and you can test pairing with Dualshock 4</h4>

<h4>Make sure Bluetooth on the Pi is turned ON. Then, press and hold <code>PS button</code> + <code>Share button</code> on Dualshock 4
Hold until the LED on the controller blinks rapidly</h4>

<h2>Step 6:</h2> 

<b>On the terminal run this command:</b>

<code>sudo ds4drv</code>

<b>If everything is correct, the Pi will detect the controller. Now you can retry <code>Step 2</code> to test the Dualshock 4</b>

<code>jstest /dev/input/js0</code>

<b>*************************************************************************************************</b>

<h2>Step 7:</h2> 

<b>[IMPORTANT] Now configure ds4drv to run at startup by editing the rc.local file:</b>

<code>sudo nano /etc/rc.local</code>

<b>After the <code># By default this script does nothing.</code> line, add a new line with the contents:</b>

<code>/usr/local/bin/ds4drv &</code>

<h2>Step 8:</h2> 

<b>Now just reboot the Pi so that the driver will be started at boot.</b>

<b>Once rebooted, enter command in Step 9 to check if the <code>ds4drv</code> driver is running in the background as root.</b>

<h2>Step 9:</h2> 

<code>ps aux | grep python</code>
