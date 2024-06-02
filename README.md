# Parking-Lot-System

## Introduction
The Internet of Things (IoT) is a crucial area of technological development today, enabling the exchange of information and intelligent control between various devices connected to the internet. The smart parking system is a typical example of IoT applications, aimed at improving the efficiency and convenience of parking management. This project introduces an Arduino UNO and ESP32-based smart parking system. The system uses an ultrasonic sensor to detect vehicles, and a camera to capture images, which are then processed on a computer using Python to recognize license plates. Indicator lights guide vehicle parking operations.

## Features
- Vehicle Detection: Uses ultrasonic sensors to detect the presence of vehicles.
- License Plate Recognition: Captures and processes images using a camera and Python-based OCR.
- Parking Guidance: Provides visual indicators to guide parking operations.

## Viewing Results
No Car Detected
When no car is detected, the system will display the following:
![no_car](https://github.com/nighteraser/Parking-Lot-System/assets/110598750/3dd21df3-ebb3-43d4-aae4-baf3f184f062)

## Installation
### Arduino UNO
1. Install the Arduino IDE from the official Arduino website.
2. Open the main.ino file in the Arduino IDE.
3. Connect your Arduino UNO to your computer.
4. Select the correct port and board from the Tools menu.
5. Upload the main.ino sketch to your Arduino UNO.
### ESP32
1. Install the ESP32 board in the Arduino IDE following these instructions.
2. Open the CameraWebServer.ino file in the Arduino IDE.
3. Set up your ESP32 with your Wi-Fi credentials in the CameraWebServer.ino file.
4. Connect the ESP32 to your computer.
5. Select the correct port and ESP32 board from the Tools menu.
6. Upload the CameraWebServer.ino sketch to your ESP32.
### Python Script
1. Install the required Python packages using pip:
``` sh
pip install easyocr opencv-python pillow pyserial
```
2. Update the IP address of your ESP32 and the Arduino port in the Python script.

## Configuration
- IP Address: Update the IP address in the Python script to match the IP address of your ESP32.
- Arduino Port: Update the port in the Python script to match the port your Arduino UNO is connected to.
## Running the System
Run the Python script to start the smart parking system. The script will connect to the ESP32 camera stream, capture images, detect car plates, and send signals to the Arduino UNO.
``` sh
python CarPlateViewer.py
```
## Dependencies
Arduino IDE: For programming the Arduino UNO and ESP32.
Python 3.x: For running the image processing and license plate recognition script.
easyocr: For Optical Character Recognition (OCR) to detect license plates.
opencv-python: For image processing.
pillow: For image handling.
pyserial: For serial communication between the computer and Arduino UNO.
