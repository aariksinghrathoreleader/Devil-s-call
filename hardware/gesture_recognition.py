import cv2
import mediapipe as mp
import numpy as np

class GestureRecognition:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils

    def detect_gesture(self, frame):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks]
                return self.classify_gesture(landmarks)
        return None

    def classify_gesture(self, landmarks):
        # Extract relevant landmarks
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        wrist = landmarks[0]

        # Rotation gestures
        if thumb_tip[1] < index_tip[1]:  # Hand is open
            if wrist[0] < thumb_tip[0]:  # Leftward swipe
                return "ROTATE_LEFT"
            elif wrist[0] > thumb_tip[0]:  # Rightward swipe
                return "ROTATE_RIGHT"
            elif wrist[1] < thumb_tip[1]:  # Upward swipe
                return "ROTATE_UP"
            elif wrist[1] > thumb_tip[1]:  # Downward swipe
                return "ROTATE_DOWN"

        # Scaling gestures
        hand_distance = np.linalg.norm(np.array(landmarks[4]) - np.array(landmarks[8]))
        if hand_distance < 0.1:  # Hands close together
            return "SCALE_DOWN"
        elif hand_distance > 0.2:  # Hands spread apart
            return "SCALE_UP"

        # Translation gestures
        if thumb_tip[1] < wrist[1]:  # Hand is above wrist
            return "MOVE_UP"
        elif thumb_tip[1] > wrist[1]:  # Hand is below wrist
            return "MOVE_DOWN"
        elif thumb_tip[0] < wrist[0]:  # Hand is to the left of wrist
            return "MOVE_LEFT"
        elif thumb_tip[0] > wrist[0]:  # Hand is to the right of wrist
            return "MOVE_RIGHT"

        # Object selection gesture
        if thumb_tip[0] < index_tip[0]:  # Swipe left
            return "SWIPE_LEFT"
        elif thumb_tip[0] > index_tip[0]:  # Swipe right
            return "SWIPE_RIGHT"

        # Toggle display gesture
        if thumb_tip[1] < wrist[1] and thumb_tip[0] == wrist[0]:  # Open palm facing camera
            return "TOGGLE_DISPLAY"

        # Confirm selection gesture
        if index_tip[1] < thumb_tip[1]:  # Pointing gesture
            return "CONFIRM_SELECTION"

        # Reset gesture (double-tap detection)
        if self.is_double_tap(landmarks):
            return "RESET"

        return "UNKNOWN"

    def is_double_tap(self, landmarks):
        # Implement logic to detect double-tap gesture
        # This is a placeholder; you can implement your own logic based on timing and position
        return False

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)  # Use 0 for the default camera
    recognizer = GestureRecognition()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gesture = recognizer.detect_gesture(frame)
        if gesture:
            cv2.putText(frame, f"Gesture: {gesture}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv2.imshow("Gesture Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
