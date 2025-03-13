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
                landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
                return self.classify_gesture(landmarks)
        return None

    def classify_gesture(self, landmarks):
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]

        if thumb_tip[1] < index_tip[1] and thumb_tip[1] < middle_tip[1]:
            return "OPEN_HAND"
        elif index_tip[1] < thumb_tip[1] and middle_tip[1] < thumb_tip[1]:
            return "POINTING"
        return "UNKNOWN"

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
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
