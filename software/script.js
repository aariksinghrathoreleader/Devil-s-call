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
