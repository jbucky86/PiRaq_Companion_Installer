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

echo --------------------------------------------chrome kiosk
sudo /bin/sh -c "cat <<EOF > /home/pi/kiosk.sh
#!/bin/bash
xset s noblank
xset s off
xset -dpms

unclutter -idle 0.5 -root &

sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/pi/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/pi/.config/chromium/Default/Preferences

/usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk --force-device-scale-factor=0.35 http://127.0.0.1:8000/tablet.html

while true; do
   xdotool keydown ctrl+r; xdotool keyup ctrl+r;
   sleep 10
done
EOF"

echo --------------------------------------------Make kiosk executable and boot
sudo chmod u+x /home/pi/kiosk.sh
sudo /bin/sh -c "cat <<EOF > /home/pi/.config/lxsession/LXDE-pi/autostart
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
#@xscreensaver -no-splash
@point-rpi
@bash /home/pi/kiosk.sh
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

echo --------------------------------------------echo Done!
echo --------------------------------------------echo rebooting in 5 seconds
sleep 5

sudo reboot

 

