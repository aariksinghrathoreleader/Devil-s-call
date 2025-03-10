import time
import picamera
from gesture_recognition import main as gesture_main
from image_processing import process_image, display_image

# Function to capture an image
def capture_image():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.start_preview()
        time.sleep(2)  # Allow camera to adjust
        camera.capture('image.jpg')
        camera.stop_preview()

# Main function
if __name__ == "__main__":
    capture_image()  # Capture an image
    process_image('image.jpg')  # Process the captured image
    display_image('processed_image.jpg')  # Display the processed image
    
    # Start gesture recognition
    gesture_main()  # Start gesture recognition
