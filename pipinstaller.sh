#!/bin/bash

# Update package list
sudo apt update

# Install Python and pip
sudo apt install -y python3 python3-pip

# Install required packages
sudo pip3 install pandas openpyxl fpdf qrcode pillow multiprocessing nicegui --break-system-packages

echo "Installation complete!"