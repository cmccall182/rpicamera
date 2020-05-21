#!/bin/bash
sudo chmod +x ./build/MLX90640
sudo cp ./MLX90640.service /lib/systemd/system/
sudo cp ./build/MLX90640 /usr/bin/
sudo chmod 644 /lib/systemd/system/MLX90640.service
sudo systemctl daemon-reload
sudo systemctl enable MLX90640.service
sudo systemctl start MLX90640.service
sudo systemctl status MLX90640.service
#Check status
#sudo systemctl status MLX90621.service

#Start service
#sudo systemctl start MLX90621.service

#Stop service
#sudo systemctl stop MLX90621.service

#Check service's log
#sudo journalctl -f -u MLX90621.service


