import threading
import time
import cv2
from gesture_recognition import GestureRecognition
from image_processing import ImageProcessor

class HologramSystem:
    def __init__(self):
        self.gesture_recognizer = GestureRecognition()
        self.image_processor = ImageProcessor()
        self.running = True

    def start_gesture_tracking(self):
        cap = cv2.VideoCapture(0)
        while self.running:
            ret, frame = cap.read()
            if not ret:
                continue

            gesture = self.gesture_recognizer.detect_gesture(frame)
            if gesture:
                print(f"Detected Gesture: {gesture}")

            cv2.imshow("Gesture Tracking", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False

        cap.release()
        cv2.destroyAllWindows()

    def process_hologram_image(self, image_path):
        sharpened, edges = self.image_processor.process_image(image_path)
        self.image_processor.save_processed_images(sharpened, edges, "hologram_output")

    def run(self):
        gesture_thread = threading.Thread(target=self.start_gesture_tracking)
        gesture_thread.start()

        while self.running:
            time.sleep(1)

        gesture_thread.join()

if __name__ == "__main__":
    system = HologramSystem()
    system.run()
