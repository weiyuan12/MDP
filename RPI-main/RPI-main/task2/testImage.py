import time
import imagezmq
from picamera2 import Picamera2, Preview
import numpy as np
import cv2
import socket
from imutils.video import VideoStream

count=0
HOST = '192.168.34.13'
PORT = '5555'
sender = imagezmq.ImageSender(connect_to=HOST+":"+PORT)
rpi_name = socket.gethostname()
cam = PiCamera()
cam.resolution = (1280,720)
cam.start_preview()
print("[Image] Start Taking Photo")
time.sleep(1.0)
while count<2:
        time.sleep(2)
        start = time.time()
        image = cam.capture_array()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
        end = time.time()
        print(f"[Image] Finished taking picture and sending photo... time took: {end - start}")
        start = time.time()
        result = sender.send_image(rpi_name, image)
        end = time.time()
        print(f"[Main] Received result: {result}, time took: {end - start}")
        if b'38' in result:
            print("Result is R")
            count += 1
        elif b'39' in result:
            print("Result is L")
            count += 1
        else:
            print("Nothing Detected!")
cam.stop_preview()