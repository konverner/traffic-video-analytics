import os
import shutil
import time
from datetime import datetime

import cv2
import pandas as pd

from nomeroff_net import pipeline
from nomeroff_net.tools import unzip
from nomeroff_net.pipes.number_plate_classificators.options_detector import CLASS_REGION_ALL


class Processor:
    def __init__(self):

        # Initialize the number plate detection and reading pipeline
        self.pipeline = pipeline("number_plate_detection_and_reading",
          presets={
            "ru": {
                "for_regions": CLASS_REGION_ALL,
                "model_path": "latest"
            },
          },
          default_label="ru",
          default_lines_count=1,
          # if you not need detect region or count lines
          off_number_plate_classification=True,
          image_loader="opencv"
        )

    # Function to process frames, extract number plate texts, and display the results
    def one_video_run(self, video_path, process_interval, output_dir):

        idx = 0

        results = {
            "source": [],
            "timestamp": [],
            "number_plate": [],
            "confidence": [],
            "image_path": []
        }

        # Create a temporary directory to store frames
        temp_dir = "tmp"
        os.makedirs(temp_dir, exist_ok=True)

        # We create a directory to store the outputs for the given video
        video_name = os.path.basename(video_path)
        outputs = f"{output_dir}/images/{video_name}"
        os.makedirs(outputs, exist_ok=True)

        # Open video file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Cannot open video.")
            return

        last_time = time.time()
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            current_time = time.time()

            if current_time - last_time >= process_interval:
                last_time = current_time

                # Save the current frame as an image
                frame_path = os.path.join(temp_dir, f"frame_{frame_count}.jpg")
                try:
                    cv2.imwrite(frame_path, frame)
                except:
                    continue

                # Process the saved frame
                (images, images_bboxs,
                 images_points, images_zones, region_ids,
                 region_names, count_lines,
                 confidences, texts) = unzip(self.pipeline([frame_path]))

                previous_text = None

                # Draw rectangles and texts on the frame
                for bbox, text in zip(images_bboxs[0], texts[0]):

                    # if we get the same text as previously, we skip it
                    if text == previous_text:
                        previous_text = text
                        continue

                    # extract a crop of detected plate from the frame
                    top_left = (int(bbox[0]), int(bbox[1]))
                    bottom_right = (int(bbox[2]), int(bbox[3]))
                    target_frame = cv2.imread(
                        frame_path
                    )#[top_left[1]:bottom_right[1] + 520, top_left[0]:bottom_right[0] + 550]
                    cv2.imwrite(os.path.join(outputs, f"plate-{idx}.jpg"), target_frame)
                    idx += 1

                    # frame = cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
                    # frame = cv2.putText(frame, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    #             0.8, (0, 255, 0), 2, cv2.LINE_AA)

                    # Save all infromation into result table
                    results["source"].append(video_path)
                    results["timestamp"].append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    results["number_plate"].append(text)
                    results["confidence"].append(bbox[4])
                    results["image_path"].append(frame_path)
                # Delete the temporary image file to save disk space
                os.remove(frame_path)

            # Display the resulting frame
            #cv2.imshow('Video Frame', frame)

            # Increment frame count
            frame_count += 1

            # Press 'q' to quit the video window before it ends
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

        # Release the video capture object and close windows
        cap.release()
        #cv2.destroyAllWindows()

        # Remove the temporary directory and its contents
        shutil.rmtree(temp_dir)
        return pd.DataFrame(results)
