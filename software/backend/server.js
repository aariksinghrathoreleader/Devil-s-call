const express = require('express');
const multer = require('multer');
const http = require('http');
const WebSocket = require('ws');
const admin = require('firebase-admin');
require('dotenv').config();
const { spawn } = require('child_process');

// Initialize Firebase
const serviceAccount = require('./firebase-adminsdk.json');
admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    storageBucket: process.env.FIREBASE_STORAGE_BUCKET
});
const bucket = admin.storage().bucket();

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

app.use(express.json());

const storage = multer.memoryStorage();
const upload = multer({ storage });

// Upload image to Firebase & process
app.post('/upload', upload.single('image'), async (req, res) => {
    if (!req.file) return res.status(400).json({ error: 'No file uploaded' });

    try {
        const fileName = `uploads/${Date.now()}_${req.file.originalname}`;
        const file = bucket.file(fileName);
        await file.save(req.file.buffer, { metadata: { contentType: req.file.mimetype } });

        const publicUrl = `https://storage.googleapis.com/${process.env.FIREBASE_STORAGE_BUCKET}/${fileName}`;
        res.json({ message: 'File uploaded', url: publicUrl });
    } catch (error) {
        res.status(500).json({ error: 'Upload failed', details: error.message });
    }
});

// Process image to generate 3D hologram
app.post('/process-image', (req, res) => {
    const imageUrl = req.body.imageUrl;
    if (!imageUrl) return res.status(400).json({ error: 'No image URL provided' });

    const process = spawn('python3', ['image_processing.py', imageUrl]);

    let output = '';
    process.stdout.on('data', (data) => {
        output += data.toString();
    });

    process.stderr.on('data', (data) => {
        console.error(`Processing Error: ${data}`);
    });

    process.on('close', (code) => {
        if (code === 0) {
            try {
                const result = JSON.parse(output.trim());
                res.json({ message: '3D hologram generated', modelUrl: result.modelUrl });
            } catch (err) {
                res.status(500).json({ error: 'Invalid AI response' });
            }
        } else {
            res.status(500).json({ error: 'Image processing failed' });
        }
    });
});

// WebSocket for real-time gesture recognition
wss.on('connection', (ws) => {
    console.log('Client connected');
    ws.on('message', (message) => {
        console.log(`Received: ${message}`);
        // Handle gesture messages here
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
