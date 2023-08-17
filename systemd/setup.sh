#/bin/bash

sudo systemctl stop mizzle.path

sudo cp mizzle.service /etc/systemd/system/
sudo cp mizzle.path /etc/systemd/system/

sudo systemctl start mizzle.path
sudo systemctl preset mizzle.path

