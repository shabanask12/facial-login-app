// Get references to all our HTML elements
const video = document.getElementById('webcam');
const loginButton = document.getElementById('login-button');
const statusMsg = document.getElementById('status');
const canvas = document.getElementById('snapshot');
const context = canvas.getContext('2d');

// --- 1. Start the Webcam ---
// This asks the user for permission to use their camera
async function startWebcam() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { width: 640, height: 480 },
            audio: false 
        });
        video.srcObject = stream;
    } catch (err) {
        console.error("Error accessing webcam: ", err);
        statusMsg.textContent = "Error: Could not access webcam.";
    }
}

// --- 2. Add Login Button Event ---
// When the button is clicked, run the 'login' function
loginButton.addEventListener('click', login);

async function login() {
    statusMsg.textContent = "Identifying...";
    statusMsg.style.color = "#555";

    // --- 3. Take a Snapshot ---
    // Set canvas size to match video and draw the current frame
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert the snapshot to a Base64 image string
    const imageDataURL = canvas.toDataURL('image/jpeg');

    // --- 4. Send the Snapshot to the Backend ---
    // This is the most important part. We 'fetch' our Python server's API.
    // This /api/login endpoint doesn't exist *yet*. We'll build it next.
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageDataURL })
        });

        const result = await response.json();

        // --- 5. Handle the Backend's Response ---
        if (result.success) {
            statusMsg.textContent = `Welcome, ${result.name}! Access granted.`;
            statusMsg.style.color = "green";
        } else {
            statusMsg.textContent = "Access Denied: Face not recognized.";
            statusMsg.style.color = "red";
        }

    } catch (error) {
        console.error("Error during login request: ", error);
        statusMsg.textContent = "Error: Could not connect to server.";
        statusMsg.style.color = "red";
    }
}

// Start the webcam as soon as the page loads
startWebcam();