'''
test_main.py

This file is the modified verison of main.py. My current idea is after start, the robot first execute SF030 or something while the image starts to take pictures every second
until it sees anything. Rpi then sends L/R to stm and waits for its ack, after receiving the ack it continues to take the image for second obsatcle every second...
After detecting obsatcles twice successfully, the cam will close, this code will finish until stm sends D or something indicating done.
'''

import time

from bluetoothapi import BluetoothAPI
from serialapi import SerialAPI
import RPi.GPIO as GPIO
import socket
import imagezmq
from picamera import PiCamera
from picamera.array import PiRGBArray

# global constants
HOST = '192.168.34.13'
PORT = '5555'

# take image every second, it keeps taking image until it sees 38/39
def take_image():
    global sender, rpi_name
    try:
        while True:
            # take the image
            output = PiRGBArray(cam)
            cam.capture(output, 'bgr')
            image = output.array
            output.truncate(0)  # Clear the output for next frame

            # send image to image server and get prediction result
            result = sender.send_image(rpi_name, image)
            result = result.decode('utf-8')     

            if str(result) in ['38', '39']: # either right or left
                print("[Main] Detected:", result)
                return str(result)
            time.sleep(0.5)
    except Exception as error:
        print(f"[Main] Get error from take_image: {error}")


# take image every second until it recognizes any arrow
def read_image():
    global obstacleCount
    global sender, rpi_name
    try:
        while obstacleCount:
                result = take_image()
                send_message = 'R' if result == '38' else 'L'
                print("[Main] Sending", send_message, "to STM")
                serialapi.write(send_message.encode("utf-8"))
                ack = None
                while not ack:
                    ack = serialapi.read()
                    print(f"[Main] Received from STM: {ack}")
                obstacleCount -= 1
    except Exception as error:
        print(f"[Main] Get error from read_image: {error}")


#Function to read messages for bluetooth and stop the function after start is read
def read_bluetooth():
    message = bluetoothapi.read()   # block until receive any data, read start message from android side
    if not message or len(message) == 0:
        print("[Main] Invalid message from bluetooth: ", message)
        exit()
    
    print("[Main] Message recieved from bluetooth", message)
    
    serialapi.write("S".encode('utf-8'))    # send start info to stm


if __name__ == "__main__":
    obstacleCount = 2

    GPIO.cleanup()
    time.sleep(0.5)

    # initialize api
    bluetoothapi = BluetoothAPI()
    serialapi = SerialAPI()

    # start the camera
    cam = PiCamera()
    cam.resolution = (1280,720)
    cam.awb_mode = 'auto'
    cam.exposure_mode = 'backlight'
    #config = cam.create_preview_configuration(main={"size":(1000,1000)})   # Set the size of the preview
    #cam.configure(config)
    #cam.start()
    print("[Image] Start Camera")

    # connect to image server
    sender = imagezmq.ImageSender(connect_to="tcp://"+HOST+":"+PORT)
    rpi_name = socket.gethostname()

    bluetoothapi.connect()
    serialapi.connect()
    print("[Main] Attempting to start...")
    read_bluetooth()

    cam.close()

    # wait until stm sends 'D':
    message = serialapi.read()
    while b'D' not in message:
        pass
    print("[Main] Task finished")


    
