import cv2
import numpy as np
import sys

# Load the DNN model
modelFile = "models/res10_300x300_ssd_iter_140000.caffemodel"
configFile = "models/deploy.prototxt.txt"
net = cv2.dnn.readNetFromCaffe(configFile, modelFile)

# Open a handle to the default webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    sys.exit("Failed to open the webcam!")

# Flag to check if an image has been saved
image_saved = False

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Prepare the frame for detection
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))

    # Detect faces in the frame
    net.setInput(blob)
    detections = net.forward()

    # Loop over the detections
    for i in range(0, detections.shape[2]):
        # Extract the confidence (i.e., probability) associated with the detection
        confidence = detections[0, 0, i, 2]

        # Filter out weak detections
        if confidence > 0.5 and not image_saved:
            # Compute the (x, y)-coordinates of the bounding box for the face
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # Draw a rectangle around the face
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

            # Save the full image with the rectangle(s)
            cv2.imwrite("detected_faces.jpg", frame)
            print("Image with detected faces saved.")
            image_saved = True
            break  # Break from the loop after saving the image

    # Display the frame
    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
