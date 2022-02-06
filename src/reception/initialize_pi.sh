#!/bin/bash
set -euxo pipefail

cd /home/pi

#install barlow
wget https://www.1001fonts.com/download/barlow.zip
mkdir .fonts
mv barlow.zip .fonts
sudo fc-cache -f -v

#hide cursor
sudo echo 'xserver-command = X -nocursor' >> sudo /etc/lightdm/lightdm.conf

# install venv
sudo apt-get update
sudo apt-get install python3-venv

#clone repo
git clone https://github.com/tman137/foodhub-reception.git
cd foodhub-reception
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements_reception.txt

#set start script on startup
echo 'cd foodhub-reception' >> ~/.bashrc
echo 'source .venv/bin/activate' >> ~/.bashrc
echo 'python3 src/reception/reception.py $1 $2 $3 $4' >> ~/.bashrc

sudo reboot
