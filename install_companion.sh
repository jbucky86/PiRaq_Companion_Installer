#!/bin/bash
#Update and install node, npn, git and so on
sudo apt-get update && sudo apt-get -y install nodejs npm git build-essential libudev-dev libusb-1.0-0-dev

echo Install yarn
curl -o- -L https://yarnpkg.com/install.sh | bash
export PATH="$HOME/.yarn/bin:$HOME/.config/yarn/global/node_modules/.bin:$PATH"

echo Clone companion
git clone https://github.com/bitfocus/companion.git

echo Update and build
cd companion
./tools/update.sh
./tools/build_writefile.sh
cd

echo Update rules: Cant seem do without sudo su?
sudo su
cat > /etc/udev/rules.d/50-companion.rules <<EOF
SUBSYSTEM=="input", GROUP="input", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0060", MODE:="666", GROUP="plugdev"
KERNEL=="hidraw", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0060", MODE:="666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTRS{idVendor}=="ffff", ATTRS{idProduct}=="1f40", MODE:="666", GROUP="plugdev"
KERNEL=="hidraw", ATTRS{idVendor}=="ffff", ATTRS{idProduct}=="1f40", MODE:="666", GROUP="plugdev"
EOF
exit

