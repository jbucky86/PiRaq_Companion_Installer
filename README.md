# PiRaq_Companion_Installer
script to install companion on RPi 3 with a PiRaq . 

use PiRaq image https://drive.google.com/open?id=1afkOQGkFdZRpDQW7yNO8YGyvY-oKoni2

connect pi to the internet

ssh into pi or use a keyboad to run 

curl https://raw.githubusercontent.com/jbucky86/PiRaq_Companion_Installer/bucky/PiRaqCompanion.sh| bash

it will take a while but that should take care of everthing



The encoder will scroll the webpage

center button will use button 12 on page 99

up will jump up 

down will jump down 

left will goto top of page

right will goto bottom 

hold right and hit center button will change the Pi Ip addreas to 192.168.86.4 

hold left and hit center button will set the rpi to DHCP. if dhcp fails it will revert to 192.168.1.2

hold left and right will reboot rpi

i havent found a way to get it to the size i want by default so if you hold down and use the encodor it will zoom the screen or youll need to plug in a keyboard and use ctrl+(-) to size it. this only needs to be done once chrome will save the size.  To have all 12 button from one page on the screen at once set it to 80%

The rest is on you 
