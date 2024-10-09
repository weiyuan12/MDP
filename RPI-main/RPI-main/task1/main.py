import multiprocessing
import time
import threading

from bluetoothapi import BluetoothAPI
from ipsocketapi import IPSocketAPI
from serialapi import SerialAPI
from imageapi import ImageAPI
import RPi.GPIO as GPIO
import atexit
import queue

'''Format sent from Algo E.g P___6 (direction, pad,pad,pad,index)'''
'''Initial Android format E.g ALG:8,1,S,0;14,1,W,1;1,2,S,2;'''
# ALG:START9


class Multithreader:

    def __init__(self):
        """
        The function initializes several APIs and creates a queue and a variable for obstacle
        identification.
        """
        self.bluetoothapi = BluetoothAPI()
        self.ipsocketapi = IPSocketAPI()
        self.serialapi = SerialAPI()
        self.imageClientapi = ImageAPI()
        self.write_message_queue = multiprocessing.Queue()
        self.obstacle_id = None

    # Function to start all the threads
    def initialize_processes(self):
        """
        The `initialize_processes` function initializes and starts multiple threads for reading from
        Bluetooth, IP socket, taking pictures, writing, and handling the image queue. The .join() ensures all threads complete their execution.
        """
        global takePictureNow
        global imageQueue
        print("[Main] Attempting to initialize multithreader...")
        self.serialapi.connect()
        # Connect the different components
        self.ipsocketapi.connect()
        self.bluetoothapi.connect()

        # Run the multithreading
        self.read_bluetooth_process = threading.Thread(
            target=self.read_bluetooth)
        self.read_ipsocket_process = threading.Thread(
            target=self.read_ipsocket)
        self.read_image_process = threading.Thread(target=self.takePicture)
        self.write_process = threading.Thread(target=self.write)
        self.handleIQ_process = threading.Thread(target=self.handleImageQueue)

        self.read_ipsocket_process.start()
        self.read_bluetooth_process.start()
        self.read_image_process.start()
        self.write_process.start()
        self.handleIQ_process.start()
        print("[Main] Initialized multithreader successfully")

        self.read_ipsocket_process.join()
        self.read_bluetooth_process.join()
        self.read_image_process.join()
        self.write_process.join()
        self.handleIQ_process.join()

    # Function to take picture and add to the imageQueue
    def takePicture(self):
        """
        The `takePicture` function takes a picture using the Raspberry Pi camera and adds it to the image
        queue along with the corresponding obstacle ID.
        """
        global running
        global takePictureNow
        global imageQueue

        while running:
            if takePictureNow == True:
                obstacle_id = self.obstacle_id
                print(f"[Image] Taking the picture for {obstacle_id}")
                takenPicture = self.imageClientapi.rpiTakePicture()
                print(
                    f"[Image] Successfully taken the photo for {obstacle_id}")
                #Queue taken picture and its obstacle id into image queue
                imageQueue.put([takenPicture, obstacle_id])
                takePictureNow = False
    def read_stm_with_timeout(self, timeout_event):
            global stm_ack_received
            ack = None
            while ack is None and not timeout_event.is_set():
                ack = self.serialapi.read()
                if ack and b'A' in ack:
                    stm_ack_received = True
                    return
                time.sleep(0.1) # Sleep a short duration before trying again

    # disconnect all/RPI end
    def disconnectall(self):
        """
        The function `disconnectall` disconnects from various connections and closes the camera,
        Bluetooth, and IP socket.
        :return: nothing (None).
        """
        global reccedImages
        global numObstacle
        while True:
            if len(reccedImages) == numObstacle:
                time.sleep(5)
                self.imageClientapi.sendEmptyImage()
                print("[Image] Closing camera")
                self.imageClientapi.imageClose()
                print("[Main] Disconnecting from IP Socket")
                self.ipsocketapi.server.close()
                print("[Main] Disconnecting from Bluetooth")
                self.bluetoothapi.server.shutdown(2)
                self.bluetoothapi.server.close()
                running = False
                exit()
            break
        return

    # Function to send the images to the image server and update the result when it comes back
    def handleImageQueue(self):
        """
        The `handleImageQueue` function processes images from a queue, sends them to a server for
        recognition, and handles the results accordingly.
        """
        global obstacleCounter
        global reccedImages
        global running
        while running:
            if not imageQueue.empty():
                # print(f"[Main] Current Queue: {imageQueue}")
                currentQ = imageQueue.get()
                takenPicture = currentQ[0]
                obstacle_id = currentQ[1]
                count = 0
                print("[Main] Sending Image to server")
                image_id = self.imageClientapi.sendImage(
                    takenPicture)
                image_id = str(image_id)
                print("[Main] Image ID received from server:", image_id)
                iMsg = image_id.encode('utf-8')
                obs = str(obstacle_id)
                try:
                    # error correction not implemented
                    # if the message is invalid print result
                    if (image_id == 'N'):
                        print("[Main] Print image recognition result")
                        iError = (image_id+obs).encode('utf-8')
                        print(iError)
                        
                    #if message is valid
                    elif (image_id != '99' and image_id != 'N'):
                        print("[Bluetooth] Sending the image results to android")
                        bMsg = "TARGET,"+obs+","+str(image_id)
                        print("[Bluetooth] Message sent to android:", bMsg)
                        # tell android immediately
                        self.bluetoothapi.write(bMsg)
                        # after recognise image
                        reccedImages.append(image_id)
                        obstacleCounter -= 1
                        print(
                            f"[Main] Number of obstacles left {obstacleCounter}")
                    #if bullseye just print
                    else:
                        print("[Main] Bullseye")
                        print("[Bluetooth] Sending the image results to android")
                        bMsg = "TARGET,"+obs+","+str(image_id)
                        print("[Bluetooth] Message sent to android:", bMsg)
                        # tell android immediately
                        self.bluetoothapi.write(bMsg)

                        # after recognise image
                        reccedImages.append(image_id)
                        obstacleCounter -= 1
                        print(
                            f"[Main] Number of obstacles left {obstacleCounter}")
                except Exception as mistake:
                    print("[Main] Image recognition error:", mistake)

    # Function to read messages from the Android tablet
    def read_bluetooth(self):
        """
        The function `read_bluetooth` reads messages from a Bluetooth connection and performs different
        actions based on the received messages.
        """
        global obstacleCounter
        global numObstacle
        global running
        global bluetoothOn
        global firstTime
        if self.bluetoothapi.check_connection is None:
            self.reconnect_android()
        while running and bluetoothOn:
            message = self.bluetoothapi.read()
            if message is not None and len(message) > 0:
                print("[Main] Message received from bluetooth", message)
                try:
                    if b'START' in message:
                        firstTime = False
                        print("[Main] Starting to dequeue")
                        self.write()

                    elif b'ALG' in message:
                        obstacles = message.decode('utf-8').split(';')
                        # print(obstacles)
                        x = 0
                        while x < len(obstacles):
                            if len(obstacles[x]) < 4:
                                obstacles.remove(obstacles[x])
                            else:
                                x += 1
                        # get rid of empty obstacles
                        filteredObstacles = ";".join(obstacles)
                        filteredObstacles = filteredObstacles+";"
                        numObstacle = len(obstacles)
                        obstacleCounter = len(obstacles)
                        print(
                            "Sending filtered obstacles directly to algo:" + filteredObstacles)
                        self.ipsocketapi.write(
                            filteredObstacles.encode('utf-8'))
                except Exception as exception:
                    print("[ERROR] Invalid message from bluetooth")
                    print(str(exception))

    # Function to read messages from Algorithm
    def read_ipsocket(self):
        """
        The function `read_ipsocket` reads messages from an IP socket, processes them, and adds them to
        a message queue for further processing.
        """
        global running
        #read from algo first time
        while running and firstTime:
            message = self.ipsocketapi.read()
            if message is not None and len(message) > 0:
                n = 5
                instr = [message[i:i+n] for i in range(0, len(message), n)]
                for r in instr:
                    #if scan instruction, queue scan instruction with header "P"
                    if b'P' in r:
                        image_message = self.convert_to_dict('P', r)
                        # print("[Main] Queued ", image_message,
                        #       "to image server")
                        self.write_message_queue.put(image_message)
                    # else queue instructions to STM with header "S"
                    else:
                        print("[Main] Queueing message to be sent to STM:", r)
                        stm_message = self.convert_to_dict('S', r)
                        self.write_message_queue.put(stm_message)
                        androidToSend = "COMMAND," + (r.decode('utf-8'))
                        androidToSend = androidToSend.encode('utf-8')
                        and_message = self.convert_to_dict('B', androidToSend)
                        self.write_message_queue.put(and_message)
                print(
                    f"[Main] Queue to send: {self.write_message_queue}")
            else:
                print("[Main] Invalid command", message, "read from Algo")

    # Protocol to reconnect with Android tablet
    def reconnect_android(self):
        """
        The function attempts to reconnect to an Android device via Bluetooth and starts reading and
        writing processes.
        """
        print("[Main] Attempting to reconnect")
        self.bluetoothapi.disconnect()

        global writeOn
        global bluetoothOn
        writeOn = False
        bluetoothOn = False

        self.bluetoothapi.connect()
        print("[BT] BT successfully reconnected")

        writeOn = True
        bluetoothOn = True

        # call multiprocess and start
        self.read_android_process = threading.Thread(
            target=self.read_bluetooth)
        self.read_android_process.start()
        self.read_android_process.join()
        self.write_process = threading.Thread(target=self.write)
        self.write_process.start()
        self.write_process.join()

        print("Reconnected to android...")

    # Function for writing messages to the different components
    def write(self):
        """
        The `write` function is responsible for sending messages to different devices based on their
        headers.`
        """
        global running
        global writeOn
        global firstTime
        global takePictureNow
        global stm_ack_received
        while running and writeOn and firstTime == False:
            try:
                if self.write_message_queue.empty():
                    print('[Main] Write queue is empty')
                    break
                    # continue
                # print(self.write_message_queue)
                if takePictureNow == False:
                    message = self.write_message_queue.get()
                    print("[Main] Message to send: ", message)
                    header = message["header"]
                    body = message["body"]
                    if header == "B":  # Android
                        print("[Main] Sending ", body, " to Android")
                        failed = self.bluetoothapi.write(body)
                        if failed:
                            print("[Bluetooth] Attempting to reconnect bluetooth")
                            self.reconnect_android(self)

                    elif header == "I":  # Algo
                        print("[Main] Sending", body, "to IpSocket")
                        self.ipsocketapi.write(body)

                    elif header == "P":  # Image server
                        obstacle_id = int(body[-1])-48
                        print("[Main] Obstacle ID:", str(obstacle_id))
                        self.obstacle_id = obstacle_id
                        takePictureNow = True
                        print("[Main] Going to take picture for " + str(obstacle_id))
                        #send take pic instruction to STM
                        serialmsg= ("PXXX"+str(obstacle_id)).encode('utf-8')
                        self.serialapi.write(serialmsg)
                        ack = None
                        while ack is None:
                            ack = self.serialapi.read()
                            print("[Main] Received from STM", ack)
                            if  b'A' not in ack:
                                ack = None

                    elif header == "S":  # STM
                        print(f"[Main] STM processing started with {body}")
                        try:
                            print("[Main] Sending ", body, " to STM")
                            self.serialapi.write(body)

                            # Initialize or reset the ack_received flag and timeout_event
                            stm_ack_received = False
                            timeout_event = threading.Event()

                            # Start a new  to listen for STM response with a timeout
                            stm_thread = threading.Thread(target=self.read_stm_with_timeout, args=(timeout_event,))
                            stm_thread.start()
                            stm_thread.join(timeout=10)  # This will wait for up to 10 seconds

                            # After waiting, if still no response, trigger the timeout_event to stop the stm_thread
                            if not stm_ack_received:
                                timeout_event.set()
                                stm_thread.join()  # Ensure the thread has stopped
                                print("[Main] STM did not respond in time. Proceeding to next command.")
                        except Exception as wrong:
                            # to show what is being sent
                            print("[Main] Error sending STM", body)
                            print("[Main] Error sending STM", wrong)

                    else:
                        print("[Main] Invalid header " + str(header))

                    print("[Main] Message sent")
            except Exception as exception:
                print("[Main] Error occurred in write: " + str(exception))
                time.sleep(1)

    # Converting to a dictionary to store in the queue
    def convert_to_dict(self, header, body):
        return {"header": header, "body": body}

    # Clean up operation for when the programme is closed midway
    def clean_up(self):
        GPIO.cleanup()


if __name__ == "__main__":
    # Defining global variables
    takePictureNow = False
    imageQueue = queue.Queue(10)
    obstacleCounter = None
    numObstacle = None
    reccedImages = []
    bluetoothOn = True
    writeOn = True
    running = True
    firstTime = True
    stm_ack_received = False
    # Running the programme
    mt = Multithreader()
    mt.disconnectall()
    atexit.register(mt.clean_up)

    time.sleep(2)

    mt.initialize_processes()