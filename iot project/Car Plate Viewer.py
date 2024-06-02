import tkinter as tk
from tkinter import Label, messagebox
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np
from urllib.request import urlopen
import easyocr
import serial
import time

# Configuration variables
ip = ''  # Change this to your ESP32-CAM IP
url = f"http://{ip}:81/stream"
CAMERA_BUFFER_SIZE = 2048
SERIAL_PORT = 'COM5'  # Update this to your actual port
BAUD_RATE = 9600

class CarPlateGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Plate Viewer")

        # Initialize OCR reader
        self.reader = easyocr.Reader(['en'])

        # Create widgets for video stream
        self.video_title = Label(root, text="Live Video Stream", font=("Arial", 16))
        self.video_title.pack()
        self.video_label = Label(root)
        self.video_label.pack()

        # Create widgets for captured image
        self.image_title = Label(root, text="Captured Image", font=("Arial", 16))
        self.image_title.pack()
        self.image_label = Label(root)
        self.image_label.pack()

        # Create label for displaying car plate number
        self.number_label = Label(root, text="", font=("Arial", 24))
        self.number_label.pack()

        # Start video stream
        self.start_video_stream()

    def start_video_stream(self):
        try:
            self.stream = urlopen(url)
            self.bts = b''
            self.update_video_stream()
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to the ESP32-CAM. Error: {e}")

    def update_video_stream(self):
        try:
            self.bts += self.stream.read(CAMERA_BUFFER_SIZE)
            jpghead = self.bts.find(b'\xff\xd8')
            jpgend = self.bts.find(b'\xff\xd9')
            if jpghead > -1 and jpgend > -1:
                jpg = self.bts[jpghead:jpgend+2]
                self.bts = self.bts[jpgend+2:]
                jpg = np.frombuffer(jpg, dtype=np.uint8)
                if len(jpg!=0): img = cv.imdecode(jpg, cv.IMREAD_COLOR) # debug
                img = cv.resize(img, (400, 300))
                self.current_frame = img

                # Convert image to Tkinter format
                img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
                img_pil = Image.fromarray(img_rgb)
                img_tk = ImageTk.PhotoImage(image=img_pil)

                # Update video label
                self.video_label.configure(image=img_tk)
                self.video_label.image = img_tk
        except Exception as e:
            print("Error: " + str(e))
            self.bts = b''
            try:
                self.stream = urlopen(url)
            except Exception as e:
                print("Reconnection Error: " + str(e))
        
        self.root.after(10, self.update_video_stream)

    def detect(self, image_path):
        result = self.reader.readtext(image_path)
        plate_numbers = [detection[1] for detection in result if detection[2] > 0.5]
        return plate_numbers

    def capture_and_detect(self, event=None):
        cv.imwrite("pic.jpg", self.current_frame)
        plate_numbers = self.detect("pic.jpg")
        if plate_numbers:
            self.number_label.config(text=f"Car Plate: {', '.join(plate_numbers)}")
            self.send_hi()
            self.display_captured_image("pic.jpg")
        else:
            self.number_label.config(text="No plate detected.")

    def display_captured_image(self, image_path):
        img = Image.open(image_path)
        img_tk = ImageTk.PhotoImage(img)
        self.image_label.configure(image=img_tk)
        self.image_label.image = img_tk

    def send_hi(self):
        try:
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            time.sleep(2)  # Give some time for the serial connection to establish
            ser.write("hi\n".encode('utf-8'))
            ser.close()
        except Exception as e:
            print("Serial communication error: " + str(e))

if __name__ == "__main__":
    root = tk.Tk()
    gui = CarPlateGUI(root)
    
    # Bind key 'a' to capture image and detect car plate
    root.bind('<a>', gui.capture_and_detect)
    
    root.mainloop()


