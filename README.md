# Holographic Display Project
Holographic Display Project
Overview
This project aims to create a holographic display system using a Raspberry Pi, camera module, and various software components. The system captures images, processes them, and displays them in a holographic format. It also includes gesture recognition to interact with the holographic display.

Table of Contents
Features
Hardware Components Required
Pattern Recognition
Software Components
Main Code
Gesture Recognition Code
Image Processing Code
Web Interface
Image Assets
Installation
Usage
Contributing
License
Features
Image Capture: Captures images using the Raspberry Pi camera.
Image Processing: Processes images to create a 3D effect.
Gesture Recognition: Detects hand gestures to control the holographic display.
Web Interface: Allows users to upload images and view them in a 3D hologram.
Hardware Components Required
Holographic Display/Projector:

Holographic Fan Display
Looking Glass Display
Microcontroller:

Raspberry Pi (4 Model B or 3 Model B+)
Camera Module:

Raspberry Pi Camera Module V2
USB Camera (optional)
Power Supply:

5V power supply for Raspberry Pi
Appropriate power supply for the holographic display
Connectivity Module (Optional):

Wi-Fi Module (ESP8266)
Bluetooth Module (HC-05)
Enclosure:

Box or case to house components
Wires and Connectors:

Jumper wires, breadboard, and connectors
Optional Components:

Micro SD Card (at least 16GB)
Heat Sink/Fan
HDMI Cable
Pattern Recognition
The pattern recognition component of this project utilizes computer vision techniques to detect hand gestures and other patterns in real-time. This allows users to interact with the holographic display intuitively. The gesture recognition is implemented using OpenCV and a pre-trained hand detection model.

Software Components
Main Code (main.py)
python
Run
Copy code
import time
import picamera
import cv2
from gesture_recognition import main as gesture_main
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
Gesture Recognition Code (gesture_recognition.py)
python
Run
Copy code
import cv2

hand_cascade = cv2.CascadeClassifier('path_to_hand_cascade.xml')

def detect_hand(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hands = hand_cascade.detectMultiScale(gray, 1.1, 5)
    return hands

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hands = detect_hand(frame)

        for (x, y, w, h) in hands:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            if w > 100:
                print("Zooming In")
            elif w < 50:
                print("Zooming Out")
            elif x < 50:
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
Image Processing Code (image_processing.py)
python
Run
Copy code
import cv2

def process_image(image_path):
    img = cv2.imread(image_path)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('processed_image.jpg', gray_img)

def display_image(image_path):
    pass  # Replace with actual code to interface with the display
Web Interface (HTML, CSS, JavaScript)
HTML (index.html)
html
Run
Copy code
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Hologram Viewer</title>
    <link rel="stylesheet" href="styles.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="splash-screen">
        <h1 id="logo">Devil's Call</h1>
    </div>
    <div id="app" style="display: none;">
        <header>
            <h1>3D Hologram Viewer</h1>
            <div id="devils-call">😈 Devil's Call</div>
        </header>
        <div id="upload-container">
            <input type="file" id="file-input" accept="image/*">
            <button id="upload-button">Upload</button>
            <button id="create-magic-button">Create Magic</button>
        </div>
        <div id="pointsDisplay">Points: 0</div>
        <div id="hologram-container"></div>
    </div>
    <script src="script.js"></script>
</body>
</html>
CSS (styles.css)
css
Run
Copy code
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    overflow: hidden; /* Prevent scrolling during splash */
    font-family: 'Arial', sans-serif;
}

#splash-screen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #000, #444);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999; /* Ensure it covers the entire screen */
    opacity: 1;
    animation: fadeOut 2s forwards 3s; /* Fade out after 3 seconds */
}

@keyframes fadeOut {
    0% { opacity: 1; }
    100% { opacity: 0; }
}

#logo {
    font-size: 50px; /* Set font size to 50px */
    font-weight: bold; /* Make the text bold */
    color: #ff3d00; /* Bright red color for the logo */
    animation: scaleUp 1s ease-in-out forwards;
}

@keyframes scaleUp {
    0% { transform: scale(0); }
    100% { transform: scale(1); }
}

#app {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100vh;
    opacity: 0; /* Start hidden */
    transition: opacity 1s ease-in; /* Fade in */
}

header {
    width: 100%;
    padding: 20px;
    background: linear-gradient(90deg, #1a1a1a, #3a3a3a);
    text-align: center;
    position: relative;
    border-bottom: 2px solid #61dafb; /* Sci-fi border */
}

header h1 {
    margin: 0;
    font-size: 2.5em;
    text-shadow: 0 0 10px #61dafb; /* Glowing text effect */
}

#devils-call {
    position: absolute;
    top: 20px;
    right: 20px;
    color: #ff3d00; /* Bright red for the devil's call */
    font-size: 24px;
}

#upload-container {
    margin: 20px 0;
    display: flex;
    gap: 10px;
}

#upload-container input {
    padding: 10px;
    border: none;
    border-radius: 5px;
    background-color: #333; /* Dark input background */
    color: #e0e0e0; /* Light text color */
    border: 1px solid #61dafb; /* Sci-fi border */
    transition: border-color 0.3s;
}

#upload-container input:focus {
    border-color: #ff3d00; /* Highlight on focus */
}
JavaScript (script.js)
javascript
Run
Copy code
// Initialize Three.js variables
let scene, camera, renderer, mesh;
let points = 0; // Initialize points

// Function to initialize the 3D scene
function init() {
    // Create a scene
    scene = new THREE.Scene();

    // Set up a camera
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 5; // Position the camera

    // Create a WebGL renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight - 150); // Adjust height to fit header and buttons
    document.getElementById('hologram-container').appendChild(renderer.domElement);

    // Add a light to the scene
    const light = new THREE.AmbientLight(0xffffff, 0.5); // Soft white light
    scene.add(light);

    // Create a plane geometry for the hologram
    const geometry = new THREE.PlaneGeometry(3, 3);
    const material = new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide });
    mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);

    // Start the animation loop
    animate();
}

// Function to animate the scene
function animate() {
    requestAnimationFrame(animate);
    mesh.rotation.x += 0.01; // Rotate the mesh
    mesh.rotation.y += 0.01; // Rotate the mesh
    renderer.render(scene, camera);
}

// Handle file upload
document.getElementById('upload-button').addEventListener('click', () => {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('photo', file);

        // Send the image to the server
        fetch('/api/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Update points (for example, increment by 1 for each upload)
            points += 1;
            document.getElementById('pointsDisplay').innerText = `Points: ${points}`;
            // Load the uploaded image as a texture
            const texture = new THREE.TextureLoader().load(data.imagePath, function(texture) {
                mesh.material.map = texture; // Set the uploaded image as the texture
                mesh.material.needsUpdate = true; // Update the material
            });
        })
        .catch(error => {
            console.error('Error uploading image:', error);
        });
    }
});

// Function to handle splash screen fade out
function handleSplashScreen() {
    const splashScreen = document.getElementById('splash-screen');
    const app = document.getElementById('app');

    // Wait for the splash screen animation to finish
    setTimeout(() => {
        splashScreen.style.display = 'none'; // Hide splash screen
        app.style.display = 'flex'; // Show the app
        app.style.opacity = 1; // Fade in the app
    }, 5000); // Adjust time as needed
}

// Initialize the scene and handle splash screen
init();
handleSplashScreen();
Image Assets
Place any required image assets in the images directory. Ensure that the paths in the code reference these images correctly.
Installation
Clone the repository:

bash
Run
Copy code
git clone https://github.com/yourusername/holographic-display.git
cd holographic-display
Install required libraries:

bash
Run
Copy code
pip install opencv-python picamera
Set up the Raspberry Pi and connect the camera module.

Ensure you have the necessary image assets and the hand cascade XML file in the correct paths.

Usage
Run the main code:

bash
Run
Copy code
python main.py
Use the web interface to upload images and interact with the holographic display.

Use hand gestures to control the display (zoom in/out, close the hologram).

Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

License
This project is licensed under the Apache License Version 2.0. See the LICENSE file for details.
