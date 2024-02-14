import cv2
import threading

def capture_frames():
    # Create a VideoCapture object
    cap = cv2.VideoCapture(0)  # 0 for the default camera, you can also use 1, 2, etc. for other cameras if available

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Read and display frames from the camera
    while True:
        ret, frame = cap.read()  # Read a frame from the camera

        # Check if the frame is valid
        if not ret:
            print("Error: Cannot receive frame from camera. Exiting...")
            break

        # Display the frame
        cv2.imshow('Camera', frame)

        # Check for key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture object
    cap.release()

def main():
    # Create and start the thread for capturing frames
    capture_thread = threading.Thread(target=capture_frames)
    capture_thread.start()

    # Wait for the thread to finish
    capture_thread.join()

    # Close all OpenCV windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
