// Initialize Three.js for the main hologram
let scene, camera, renderer, mainMesh;
let points = 0;

function initHologram() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 5;

    renderer = new THREE.WebGLRenderer({ alpha: true });
    renderer.setSize(window.innerWidth, 400);
    document.getElementById('hologram-container').appendChild(renderer.domElement);

    const geometry = new THREE.BoxGeometry(3, 3, 3);
    const material = new THREE.MeshBasicMaterial({ color: 0x00ffff, wireframe: true });

    mainMesh = new THREE.Mesh(geometry, material);
    scene.add(mainMesh);

    animateHologram();
}

function animateHologram() {
    requestAnimationFrame(animateHologram);
    mainMesh.rotation.x += 0.01;
    mainMesh.rotation.y += 0.01;
    renderer.render(scene, camera);
}

// Initialize Three.js for tiles
let tileScene, tileCamera, tileRenderer;
let tiles = [];

function initTiles() {
    tileScene = new THREE.Scene();
    tileCamera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    tileCamera.position.z = 10;

    tileRenderer = new THREE.WebGLRenderer({ alpha: true });
    tileRenderer.setSize(window.innerWidth, 150);
    document.getElementById('tile-container').appendChild(tileRenderer.domElement);

    const geometry = new THREE.BoxGeometry(2, 2, 2);
    for (let i = 0; i < 5; i++) {
        const material = new THREE.MeshBasicMaterial({ color: Math.random() * 0xffffff, wireframe: true });
        const cube = new THREE.Mesh(geometry, material);
        cube.position.x = i * 4 - 8;
        tileScene.add(cube);
        tiles.push(cube);
    }

    animateTiles();
}

function animateTiles() {
    requestAnimationFrame(animateTiles);
    tiles.forEach((tile, index) => {
        tile.rotation.x += 0.01 + index * 0.002;
        tile.rotation.y += 0.01 + index * 0.002;
        tile.position.y = Math.sin(Date.now() * 0.001 + index) * 1.5;
    });
    tileRenderer.render(tileScene, tileCamera);
}

// Handle splash screen fade out
function handleSplashScreen() {
    setTimeout(() => {
        document.getElementById('splash-screen').style.display = 'none';
        document.getElementById('app').style.display = 'flex';
        document.getElementById('app').style.opacity = 1;
        initHologram();
        initTiles();
    }, 4000);
}

handleSplashScreen();
