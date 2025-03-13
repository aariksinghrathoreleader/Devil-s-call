# main.py
import time
import picamera
import cv2
from gesture_recognition import gesture_main
from image_processing import process_image, display_image

def capture_image():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.start_preview()
        time.sleep(2)
        camera.capture('image.jpg')
        camera.stop_preview()

if __name__ == "__main__":
    capture_image()
    process_image('image.jpg')
    display_image('processed_image.jpg')
    gesture_main()
