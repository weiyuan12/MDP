import imagezmq
import cv2
import numpy as np
import torch
from ultralytics import YOLO
import multiprocessing
from multiprocessing import Process
from utils import *
import config


# The `ImageProcessor` class is a Python class that processes and predicts images received from a
# Raspberry Pi using a YOLOv8 model.
class ImageProcessor:
    imageDict = {
        "1": "11",
        "2": "12",
        "3": "13",
        "4": "14",
        "5": "15",
        "6": "16",
        "7": "17",
        "8": "18",
        "9": "19",
        "A": "20",
        "B": "21",
        "C": "22",
        "D": "23",
        "E": "24",
        "F": "25",
        "G": "26",
        "H": "27",
        "S": "28",
        "T": "29",
        "U": "30",
        "V": "31",
        "W": "32",
        "X": "33",
        "Y": "34",
        "Z": "35",
        "Up_arrow": "36",
        "Down_arrow": "37",
        "Right_arrow": "38",
        "Left_arrow": "39",
        "Circle": "40",
    }
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Clean up operations can be added here, if needed
        # For now, we will leave it empty as you didn't specify any
        pass
    def cleanup_predict_folders(prefix="predict"):
        directory = os.path.join(os.getcwd(), 'runs/detect')
        # Iterate over the contents of the directory
        for folder_name in os.listdir(directory):
            folder_path = os.path.join(directory, folder_name)

            # Check if it is a folder and starts with the prefix 'predict'
            if os.path.isdir(folder_path) and folder_name.startswith("predict"):
                try:
                    # Remove the folder and all its contents
                    shutil.rmtree(folder_path)
                    print(f"[Cleanup] Deleted folder: {folder_name}")
                except Exception as e:
                    print(f"[Cleanup] Error deleting folder '{folder_name}': {e}")

    def __init__(self, port=config.DEFAULT_PORT):
        # Uncomment below if you want to load the model during initialization
        print("[PC] Loading model weights...")
        self.model = self.load_model()
        #self.model2 = self.load_yolov5_model()
        print("[PC] YoloV8 Model weights loaded!")
        self.port = port
        print(
            "[PC] ImageHub Server running, ready to receive requests for Image API & make predictions!"
        )

    def load_model(self):
        """
        Load the model from the local directory.
        """
        current_directory = os.getcwd()
        model_path = get_model_path(current_directory, "background_agnostic_final.pt")
        
        model = YOLO(model_path)
        return model
    
    def load_yolov5_model(self):
        """
        Load YOLOv5 model from PyTorch Hub or local path.
        """
        model_yolov5 = YOLO("/Weights/task1_yolov5.pt")  # Can specify path or use yolov5s
        return model_yolov5

    def receive_image(self, slug):
        try:
            rpi_name, image = self.image_hub.recv_image()
            filename = f"received_image_{slug}.jpg"
            cv2.imwrite(filename, image)
            return rpi_name, image
        except Exception as e:
            print(f"Error: {e}")
            self.restart_image_hub()
            return None, None

    def restart_image_hub(self):
        time.sleep(1)
        self.image_hub.close()
        print("[PC] ImageHub Server closed, restarting...")
        self.image_hub = imagezmq.ImageHub(open_port="tcp://*:5555", REQ_REP=True)
        print(
            "[PC] ImageHub Server restarted, ready to receive requests for Image API & make predictions!"
        )

    def process_image(self, image, slug, alpha=1.1, beta=20):
        """
        Process the image with optional parameters for contrast (alpha) and brightness (beta)
        """

        image_resized = cv2.resize(image, (640, 640))
        resized_filename = f"resized_image_{slug}.jpg"
        cv2.imwrite(resized_filename, image_resized)

        return image_resized

    def predict_image(self, image, slug):
        project_dir = "runs/detect"
        name_dir = f"predict{slug}"
        # To hide confidence of predictions
        results = self.model(
            image,
            imgsz=416,
            conf=0.2,
            save=True,
            show_conf=False,
            show_labels = False,
            project=project_dir,
            name=name_dir,
            boxes=False
        )
        names = self.model.names
        predicted_class = "99"
        max_prob = 0
        max_area = 0

        # Additional variables to store the bounding box with the max probability
        max_bbox = None

        # Tolerance for bounding box area to decide when to consider area over confidence
        AREA_TOLERANCE = config.AREA_TOLERANCE  # Adjust based on your needs

        for result in results:
            confidences = result.boxes.conf
            classes = result.boxes.cls
            bboxes = result.boxes.xyxy  # Get bounding boxes in xyxy format

            for i, confidence in enumerate(confidences):
                bbox = bboxes[i]
                area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])  # Calculate area
                current_class = names[int(classes[i])]
                print(f"[PC] Predicted Class: {current_class}, Confidence: {confidence:.2f}")
                
                # If area of the current bounding box is greater than the current maximum, update
                if area > max_area:
                    max_area = area
                    predicted_class = names[int(classes[i])]
                    max_bbox = bboxes[i]
                    max_prob = confidence
                # If the area difference is within the tolerance,
                # consider the confidence.
                elif abs(area - max_area) <= AREA_TOLERANCE:
                    if confidence > max_prob:
                        max_prob = confidence
                        predicted_class = names[int(classes[i])]
                        max_bbox = bboxes[i]
                        max_area = area

        return predicted_class, max_bbox, max_prob
    
    def run(self):
        self.image_hub = imagezmq.ImageHub(open_port=self.port, REQ_REP=True)
        numObstacles = 0
        while numObstacles < config.NO_OBSTACLES:
            print("[PC] Waiting for image from RPi...")

            # Generate a unique slug based on the current timestamp
            slug = str(int(time.time()))

            # Receive image from RPi
            rpi_name, image = self.receive_image(slug)

            print(f"[PC] Received image from {rpi_name}")
            numObstacles += 1
            if image is not None:
                detection_attempts = 0
                successful_detection = False

                # Default values for alpha and beta
                alpha = 1
                beta = 0

                processed_image = self.process_image(image, slug, alpha, beta)
                print(f"[PC] Image processed with alpha: {alpha} and beta: {beta}!")
                print("[PC] Predicting image...")

                # Make prediction on the processed image
                image_id, max_bbox, max_prob = self.predict_image(
                    processed_image, slug
                )

                # Check the prediction result
                if image_id != "99":  # Assuming '99' means no detection
                    successful_detection = True
                    print("[PC] Image predicted!")
                else:
                    print(
                        f"[PC] Detection attempt {detection_attempts} failed, enhancing image."
                    )

                # Move images after all prediction attempts or after a successful prediction
                # print(f"current directory: {os.getcwd()}")
                base_dir = os.path.join(os.getcwd(), "runs", "detect")
                #base_dir = os.getcwd()
                filenames_with_slug = [
                    f.replace(".jpg", f"_{slug}.jpg")
                    for f in ["received_image.jpg", "resized_image.jpg"]
                ]
                print("[DEBUG] Moving files: ", filenames_with_slug, "  To Directory: ", base_dir)
                move_images_to_latest_directory(base_dir, filenames_with_slug)
                # Get the path to the image in the latest directory
                img_path = get_latest_image_path("runs/detect")
                print("[DEBUG] Image Path: ", filenames_with_slug, "  To Directory: ", img_path)
                if img_path:
                    predicted_img = cv2.imread(img_path)

                    # Check if there's a bbox with max confidence, and if so, draw it on the image
                    if max_bbox is not None:
                        x1, y1, x2, y2 = map(int, max_bbox)
                        cv2.rectangle(
                            predicted_img, (x1, y1), (x2, y2), (0, 255, 0), 2
                        )  # Green bounding box with reduced width

                        # Add the class name and its confidence to the top-left corner of the bounding box
                        label = f"{image_id} {max_prob:.2f}"
                        label_size = cv2.getTextSize(
                            label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2
                        )[0]
                        background_rect_top_left = x1, y1 - label_size[1] - 10
                        background_rect_bottom_right = x1 + label_size[0], y1

                        cv2.rectangle(
                            predicted_img,
                            background_rect_top_left,
                            background_rect_bottom_right,
                            (0, 255, 0),
                            -1,
                        )  # Green rectangle for text background
                        cv2.putText(
                            predicted_img,
                            label,
                            (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (255, 255, 255),
                            2,
                        )  # White text

                        # Save the updated image
                        cv2.imwrite(img_path, predicted_img)

                # Send the appropriate reply to RPi
                
                if successful_detection:
                    image_id = self.imageDict[image_id]
                    self.image_hub.send_reply(image_id.encode("utf-8"))
                    print(f"[PC] Sent image_id {image_id} to RPi")
                else:
                    print(
                        "[PC] All attempts to detect the image failed. Sending '99' to RPi."
                    )
                    self.image_hub.send_reply(image_id.encode("utf-8"))
                    print(f"[PC] Sent image_id {image_id} to RPi")


if __name__ == "__main__":
    with ImageProcessor() as processor:
        processor.run()
        stitch_images()
        processor.cleanup_predict_folders()