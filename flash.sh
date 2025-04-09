#!/bin/bash

# Check if ampy is installed
if ! command -v ampy &> /dev/null; then
    echo "ampy is not installed. Please install it with pip: pip install adafruit-ampy"
    exit 1
fi

# Get the serial port from parameters or environment variable
PORT=$1
if [ -z "$PORT" ]; then
    PORT=${ESPTARGET}
    if [ -z "$PORT" ]; then
        echo "Error: Please specify the serial port as a parameter or set the ESPTARGET environment variable."
        exit 1
    fi
fi

# Path to the MicroPython firmware binary
FIRMWARE_PATH="ESP32_GENERIC_C3-20241129-v1.24.1.bin"

# Check if MicroPython is installed on the ESP32
echo "Checking if MicroPython is installed..."
ampy --port $PORT run "import sys; print(sys.implementation.name)" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "MicroPython is not installed. Flashing the ESP32 with MicroPython firmware..."

    # Check if esptool is installed
    if ! command -v esptool &> /dev/null; then
        echo "esptool is not installed. Please install it with pip: pip install esptool"
        exit 1
    fi

    esptool.py --port $PORT erase_flash
    esptool.py --port $PORT --baud 460800 write_flash -z 0x1000 $FIRMWARE_PATH
    echo "Flashing completed. Please reconnect the device."
    exit 0
fi

# Delete all data on the ESP32
echo "Deleting all files and directories in the root directory on the ESP32..."
for item in $(ampy --port $PORT ls); do
    # Check if the item has an extension (assuming it's a file)
    if [[ "$item" == *.* ]]; then
        echo "Removing file: $item"
        ampy --port $PORT rm $item
    else
        echo "Removing directory: $item"
        ampy --port $PORT rmdir $item
    fi
done

# Create the partitions directories on the ESP32
echo "Creating the partitions directories on the ESP32..."
ampy --port $PORT mkdir part2

# Send files from the lib directory to part1
echo "Sending files from the src directory to part1..."
ampy --port $PORT put src /part1

# Send files from the conf directory to conf
echo "Sending files from the conf directory to conf..."
ampy --port $PORT put conf /conf


# Send the main.py file
echo "Sending the main.py file..."
ampy --port $PORT put main.py

echo "Flashing completed successfully."
