import time
import threading

from bluetoothapi import BluetoothAPI
from serialapi import SerialAPI
import RPi.GPIO as GPIO
import atexit
import socket
import imagezmq
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
import numpy as np

class Multithreader:
    
    def __init__(self):
        self.bluetoothapi = BluetoothAPI()
        self.serialapi = SerialAPI()
        self.sender = imagezmq.ImageSender(connect_to="tcp://192.168.34.13:5555")
        self.rpi_name = socket.gethostname()
    
    #Function to start all the threads
    def initialize_processes(self):
        print("[Main] Attempting to initialize multithreader...")
        
        # Connect the different components
        self.serialapi.connect()
        self.bluetoothapi.connect()

        # Sending the dummy frame
        self.send_dummy_frame()

        #Run the multithreading
        self.read_bluetooth_process = threading.Thread(target=self.read_bluetooth)
        self.read_image_process = threading.Thread(target=self.read_image)

        self.read_bluetooth_process.start()
        self.read_image_process.start()
        print("[Main] Initialized multithreader successfully")

        self.read_bluetooth_process.join()
        self.read_image_process.join()
    
    # Function to take a dummy photo and send to the server during initialization
    def send_dummy_frame(self):
        cam = PiCamera()
        cam.resolution = (1280,720)
        output = PiRGBArray(cam)
        cam.capture(output, 'bgr')
        dummy_image = output.array
        print("[Image] Taking dummy frame: Starting Camera Preview and priming Image Server...")
        result = self.sender.send_image(self.rpi_name, dummy_image)
        print("[Image] Received result:", result)
        cam.close()

    #Function to take picbture, send to the image server and handle result
    def read_image(self):
        global takePic
        global running
        global start
        global setup
        global count
        try:
            if (setup):
                self.cam = PiCamera()
                self.cam.resolution = (1280,720)
                self.cam.awb_mode = 'auto'
                self.cam.exposure_mode = 'backlight'
                print("[Image] Start Camera")
                self.cam.start_preview()
                # print("[Image] Taking dummy frame: Start Camera Preview")
                # self.cam.capture(PiRGBArray(self.cam), 'bgr')
                setup=False
            while start==False and takePic==True:
                    print("[Image] Start taking photo...")
                    # time.sleep(2)
                    output = PiRGBArray(self.cam)
                    self.cam.capture(output, 'bgr')
                    image = output.array

                    output.truncate(0)  # Clear the output for next frame
                    print("[Image] Finished taking picture and sending photo...")

                    if count == 0:
                        print("STM starting...")
                        self.serialapi.write("S".encode('utf-8'))
                        count += 1
                    else:
                        print("STM continuing...")
                        self.serialapi.write("D".encode('utf-8'))
                    
                    # send image to image server and get prediction result
                    # sender = imagezmq.ImageSender(connect_to="tcp://192.168.34.13:5555")
                    # rpi_name = socket.gethostname()
                    print("[Image] Connected to Image server...")
                    # result = sender.send_image(rpi_name, image)
                    result = self.sender.send_image(self.rpi_name, image)
                    print("[Image] Received result:", result)
                    result = result.decode('utf-8')

                    if str(result) in ['38', '39']: # either left or right
                        takePic = False
                        return str(result)
                    else: # if detected nothing/bullseye
                        print("Unable to recognise!")
                        continue    # continue to take picture until recognised

        except Exception as error:
            print("Image Recognition Error!")
            print(error)


    #Function to read messages for bluetooth and stop the function after start is read
    def read_bluetooth(self):
        global takePic
        global running
        global start
        while start:
            message = self.bluetoothapi.read()
            start=False
            if message is not None and len(message) > 0:               
                print("[Main] Message recieved from bluetooth", message)
                try:
                  if b'sp' in message:
                      #start taking image
                      takePic=True
                      print("[Main] Going to Image...")
                      result = self.read_image()
                      #Tell STM to move
                      #self.serialapi.write(("S").encode("utf-8"))
                      # time.sleep(1)
                      if result == '38':
                        print("Sending R to STM")
                        self.serialapi.write("R".encode("utf-8"))
                      elif result == '39':
                        print("Sending L in STM")
                        self.serialapi.write("L".encode("utf-8"))
                      #wait for STM acknowledgement
                      ack = None
                      while ack is None:
                        ack = self.serialapi.read()
                        print("[Main] Received from STM:")
                        print(ack)
                        if b'A' in ack:
                            #start taking image
                            takePic=True
                            print("[Main] Going to Image...")
                            result = self.read_image()
                            #self.serialapi.write(("D").encode("utf-8"))
                            # time.sleep(1)
                            if result == '38':
                                print("Sending R to STM")
                                self.serialapi.write("R".encode("utf-8"))
                                break
                            elif result == '39':
                                print("Sending L in STM")
                                self.serialapi.write("L".encode("utf-8"))
                                break

                except:
                      print("[ERROR] Invalid message from bluetooth")
        exit()
                     
    #Clean up operation after we exit the programme
    def clean_up(self):
        GPIO.cleanup()
        self.cam.close()


if __name__ == "__main__":
    takePic = False
    running = True
    start = True
    setup = True
    count = 0
    currentObs = 1

    #Running the programme
    mt = Multithreader()
    atexit.register(mt.clean_up)

    # time.sleep(1)

    mt.initialize_processes()