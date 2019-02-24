#!/bin/bash

echo Create launcher script changed for eth0 attribute
cat > companionLaunch.sh  <<EOF 
#!/bin/bash
sudo python companionButtons.py & sudo -u pi /home/pi/companion/headless.js eth0 8000 
EOF


echo Make launcher executable
chmod u+x companionLaunch.sh

echo Create update script. Stops services, updates and relaunches
cat > companionUpdate.sh <<EOF 
#!/bin/bash 
sudo systemctl stop companion.service
cd companion 
./tools/update.sh 
./tools/build_writefile.sh 
cd 
sudo systemctl start companion.service
EOF

echo Make Update executable
chmod u+x companionUpdate.sh

echo Add companionLauncher to boot 
sudo su 
cat >  /etc/systemd/system/companion.service <<EOF 
[Unit]
Description=Companion service
After=network.target

[Service]
ExecStart=/home/pi/companionLaunch.sh
WorkingDirectory=/home/pi
StandardOutput=journal+console
StandardError=journal+console
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
EOF

exit

echo Enable service
sudo systemctl enable companion.service
