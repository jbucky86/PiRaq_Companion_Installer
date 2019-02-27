#!/bin/bash
sudo rm -rf /home/pi/sambaShare/AlarmClock

echo --------------------------------------------sudo apt-get chromium-browser
sudo apt-get install chromium-browser -y

echo --------------------------------------------install stuff and what ever
echo --------------------------------------------sudo apt-get purge wolfram-engine scratch scratch2 nuscratch sonic-pi idle3 -y
sudo apt-get purge wolfram-engine scratch scratch2 nuscratch sonic-pi idle3 -y

echo --------------------------------------------sudo apt-get purge smartsim java-common minecraft-pi libreoffice* -y
sudo apt-get purge smartsim java-common minecraft-pi libreoffice* -y

echo --------------------------------------------sudo apt-get clean
sudo apt-get clean

echo --------------------------------------------osudo apt-get autoremove -y
sudo apt-get autoremove -y

echo --------------------------------------------sudo apt-get update
sudo apt-get update

echo --------------------------------------------sudo apt-get upgrade
sudo apt-get upgrade -y

echo --------------------------------------------sudo apt-get install xdotool unclutter sed
sudo apt-get install xdotool unclutter sed -y

echo --------------------------------------------raspi-config
sudo raspi-config nonint do_boot_behaviour B4
sudo raspi-config nonint do_ssh 0
sudo raspi-config nonint do_expand_rootfs
sudo raspi-config nonint do_hostname PiRaq_Companion

echo --------------------------------------------splash screen
cd /home/pi/
wget https://bitfocus.io/companion/badge.png
sudo cp ~/badge.png /usr/share/plymouth/themes/pix/splash.png

echo --------------------------------------------Make kiosk executable and boot
cd /home/pi/
wget https://raw.githubusercontent.com/jbucky86/PiRaq_Companion_Installer/master/companionKiosk.sh
sudo chmod u+x /home/pi/companionKiosk.sh
sudo /bin/sh -c "cat <<EOF > /home/pi/.config/lxsession/LXDE-pi/autostart
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
#@xscreensaver -no-splash
@point-rpi
@bash /home/pi/companionKiosk.sh
EOF"

echo --------------------------------------------PiRaq touch screen
cat <<EOF > ~/.xsessionrc
#!/bin/bash
# Set coordinate transformation matrix for Pi-RAQ touch display
# (rotate left; adjust for accurate pointer tracking)
xinput set-prop 'TSC-50 DMC' 'Coordinate Transformation Matrix' 0 1.05 -0.025 -1.6 0 1.3 0 0 1
EOF

echo --------------------------------------------PiRaq GPIO 
cd /home/pi/
wget https://raw.githubusercontent.com/jbucky86/PiRaq_Companion_Installer/master/companionButtons.py

echo --------------------------------------------pip install python-uinput
sudo pip install python-uinput 

echo --------------------------------------------uinput added to modules

sudo /bin/sh -c "cat <<EOF > /etc/modules
# /etc/modules: kernel modules to load at boot time.
#
# This file contains the names of kernel modules that should be loaded

i2c-dev
uinput
EOF"

echo --------------------------------------------companion thanks to EPstudios for these 2 scripts
sudo curl https://raw.githubusercontent.com/jbucky86/PiRaq_Companion_Installer/master/install_companion.sh | bash

sudo curl https://raw.githubusercontent.com/jbucky86/PiRaq_Companion_Installer/master/launcher_companion.sh | bash

echo --------------------------------------------ip address setup
sudo apt-get install python-pip
sudo apt-get install dialog
sudo pip install python2-pythondialog
sudo git clone https://github.com/dggreenbaum/debinterface /root/.local/lib/python2.7/site-packages/debinterface
wget https://raw.githubusercontent.com/jbucky86/PiRaq_Companion_Installer/master/pydialog-interfaces.py
sudo chmod +x pydialog-interfaces.py
wget https://raw.githubusercontent.com/jbucky86/PiRaq_Companion_Installer/master/ipUpdate.sh
sudo chmod +x ipUpdate.sh
wget https://raw.githubusercontent.com/jbucky86/PiRaq_Companion_Installer/master/ipButtons.py
sudo chmod +x ipButtons.py 

echo --------------------------------------------echo Done!
echo --------------------------------------------echo rebooting in 5 seconds
sleep 5

sudo reboot

 

