# Necessary imports
import queue  # Used for holding a set of commands
from serialapi import SerialAPI  # Communication with STM
from imageapi import ImageAPI  # Image capturing and sending to server

# Define the BullseyeHandler class
class BullseyeHandler:

    # Constructor
    def __init__(self):
        print("[INFO] Initializing BullseyeHandler...")
        
        # Initialize Serial API for communication with STM
        self.serialapi = SerialAPI()
        
        # Initialize Image API for image processing tasks
        self.imageapi = ImageAPI()
        
        # Queue to hold set of instructions
        self.instruction_queue = queue.Queue()

    # Method to connect to STM
    def connect_to_stm(self):
        print("[INFO] Connecting to STM...")
        self.serialapi.connect()
        print("[INFO] Connected to STM!")

    # Method to disconnect from STM
    def disconnect_from_stm(self):
        print("[INFO] Disconnecting from STM...")
        self.serialapi.disconnect()
        print("[INFO] Disconnected from STM!")

    # Method to process instructions based on server response
    def process_instructions(self):
        print("[INFO] Processing instructions...")

        response = '99'
        while response == '99':
            # Attempt to capture an image and send it to the server
            try:
                print("[INFO] Capturing image...")
                image = self.imageapi.rpiTakePicture()

                print("[INFO] Sending captured image to server...")
                response = self.imageapi.sendImage(image)
            except Exception as e:
                print(f"[ERROR] Failed to capture and send image: {e}")
                return

            # Check server response
            if response == '99':
                print("[WARNING] Obstacle detected. Re-queuing navigation commands...")
                
                # List of commands to execute
                commands = ["RF090", "SF030", "LF090", "SB010", "LF090"]
                for cmd in commands:
                    self.instruction_queue.put(cmd)

                # Send queued commands to STM and await acknowledgment
                while not self.instruction_queue.empty():
                    instruction = self.instruction_queue.get()
                    print(f"[INFO] Processing instruction: {instruction}")
                    self.send_to_stm(instruction)
                    if not self.wait_for_ack():
                        print(f"[ERROR] Failed to receive acknowledgement for {instruction}")
                        break
            else:
                print("[INFO] No obstacle detected. Exiting the loop.")
                break

    # Method to send instruction to STM
    def send_to_stm(self, instruction):
        print(f"[INFO] Sending instruction {instruction} to STM...")
        self.serialapi.write(instruction.encode('utf-8'))

    # Method to wait for acknowledgment from STM
    def wait_for_ack(self):
        ack = None
        print("[INFO] Waiting for acknowledgment from STM...")
        
        while ack is None:
            ack = self.serialapi.read()
            if ack and b'A' in ack:
                print("[INFO] Acknowledgment received!")
                return True
        print("[WARNING] No acknowledgment received!")
        return False

# Main execution starts here
if __name__ == "__main__":
    print("[INFO] Starting BullseyeHandler main execution...")
    
    handler = BullseyeHandler()
    handler.connect_to_stm()
    try:
        handler.process_instructions()
    finally:
        # handler.disconnect_from_stm()
        print("[INFO] Cleaning up image resources...")
        handler.imageapi.imageClose()
        print("[INFO] Execution complete!")
