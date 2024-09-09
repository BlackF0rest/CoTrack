# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the Excel file into the container
COPY Verbrauchsmaterial_ELab_TRGE.xlsx /app/Verbrauchsmaterial_ELab_TRGE.xlsx

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
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

# Create a directory for custom fonts
RUN mkdir -p /usr/share/fonts/truetype/custom

# Copy the Arial Bold font into the custom fonts directory
COPY arialbd.ttf /usr/share/fonts/truetype/custom/arialbd.ttf

# Update the font cache
RUN fc-cache -f -v

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install pandas openpyxl Pillow qrcode[fork] fpdf nicegui

# Expose port 80 to the outside world
EXPOSE 80

# Command to run the inventory manager application
CMD ["python", "inventory_manager.py"]
