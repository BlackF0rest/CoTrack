# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libfontconfig1 \
    libxrender1 \
    libxext6 \
    libx11-6 \
    libopenjp2-7 \
    libtiff-dev \
    libxcb1 \
    libpng-dev \
    fonts-dejavu \
    fonts-freefont-ttf \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install pandas openpyxl Pillow qrcode[fork] fpdf nicegui

# Expose port 80 to the outside world
EXPOSE 80

# Command to run the inventory manager application
CMD ["python", "Bauteilemanager.py"]
