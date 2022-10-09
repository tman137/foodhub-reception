#!/bin/bash
set -euxo pipefail

# install dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install python3-venv -y
sudo apt install python3-sdl2 -y

cd /home/pi

#turn of screensaver
sudo chmod +w /etc/lightdm/lightdm.conf
echo '[SeatDefaults]' >> /etc/lightdm/lightdm.conf
echo 'xserver-command=X -s 0 -dpms' >> /etc/lightdm/lightdm.conf
#hide cursor
echo 'xserver-command = X -nocursor' >> /etc/lightdm/lightdm.conf

#install barlow
wget https://www.1001fonts.com/download/barlow.zip
mkdir .fonts
mv barlow.zip .fonts
cd .fonts
unzip barlow.zip
find . ! -name Barlow-Bold.ttf -delete
cd /home/pi 
sudo fc-cache -f -v


#clone repo
git clone https://github.com/tman137/foodhub-reception.git

#setup virtual environment
cd foodhub-reception
python3 -m venv .venv
source .venv/bin/activate
echo 'export PYTHONPATH="$PYTHONPATH:/home/pi/foodhub-reception"' >> .venv/bin/activate
pip install -r requirements_reception.txt

#set start script on startup
echo 'cd foodhub-reception' >> ~/.bashrc
echo 'source .venv/bin/activate' >> ~/.bashrc
echo 'export DISPLAY=:0.0' >> ~/.bashrc
echo "python3 src/reception/reception.py \"$1\" \"$2\" \"$3\" \"$4\"" >> ~/.bashrc

sudo reboot now
