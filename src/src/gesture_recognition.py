import cv2

# Load the pre-trained hand detection model (Haar cascade)
hand_cascade = cv2.CascadeClassifier('haarcascades/hand.xml')  # Update with the correct path

def detect_hand(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hands = hand_cascade.detectMultiScale(gray, 1.1, 5)
    return hands

def main():
    cap = cv2.VideoCapture(0)  # Use the appropriate camera index

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hands = detect_hand(frame)

        for (x, y, w, h) in hands:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Implement gesture recognition logic here
            if w > 100:  # Example condition for zooming in
                print("Zooming In")
            elif w < 50:  # Example condition for zooming out
                print("Zooming Out")
            elif x < 50:  # Example condition for closing the hologram
                print("Closing Hologram")
                cap.release()
                cv2.destroyAllWindows()
                return

        cv2.imshow('Hand Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
