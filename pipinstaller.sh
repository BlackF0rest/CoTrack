#!/bin/bash

# Update package list
sudo apt update

# Install Python and pip
sudo apt install -y python3 python3-pip

# Install required packages
sudo pip3 install -r requirements.txt

# Install additional packages
sudo apt install -y libopenblas-dev liblapack-dev libatlas-base-dev
sudo apt install -y libpq-dev
sudo apt install -y libssl-dev
sudo apt install -y libffi-dev
sudo apt install -y build-essential
sudo apt install -y libssl-dev libffi-dev python3-dev

# Install nicegui
sudo pip3 install nicegui

# Install openpyxl
sudo pip3 install openpyxl

# Install fpdf
sudo pip3 install fpdf

# Install qrcode
sudo pip3 install qrcode

# Install pillow
sudo pip3 install pillow

# Install timeloop
sudo pip3 install timeloop

# Install multiprocessing
sudo pip3 install multiprocessing

# Install xlsxwriter (optional)
sudo pip3 install xlsxwriter

echo "Installation complete!"