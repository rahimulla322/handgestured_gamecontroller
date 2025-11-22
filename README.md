✋ Hand Gesture Car Controller (Python + MediaPipe + OpenCV)

This project allows you to control a car or driving game using hand gestures detected via webcam — no physical controller required!
Using MediaPipe Hands, OpenCV, and PyDirectInput, it detects whether your hand is open (accelerate) or closed (brake) and sends corresponding keyboard inputs to the game.

🚀 Features:
🖐️ Gesture Recognition — Detects hand openness using the index finger position.
🎮 Game Control — Simulates key presses (W/S or Arrow keys) using pydirectinput.
⚡ Optimized Performance — Processes every few frames for faster detection.
🔁 Real-time Video Feed — Displays landmarks and gesture state live.
🧠 Configurable Thresholds — Fine-tune detection sensitivity easily.

🧩 Tech Stack:
Library	Purpose
OpenCV	Captures and displays webcam feed
MediaPipe	Hand landmark detection
PyDirectInput	Simulates key presses for game control
Keyboard	Allows exiting via keypress
Python (3.8+)	Core programming language

⚙️ Installation:
--> Install Dependencies: "pip install opencv-python mediapipe pydirectinput keyboard".

🎮 Usage:
1️⃣ Connect a Webcam
Make sure your webcam is connected and functioning.
2️⃣ Run the Script
python hand_controller.py
3️⃣ Controls
Gesture	Action	Key Sent
🖐️ Hand Open (Index up)	Accelerate	Right Arrow or W
✊ Hand Closed (Index down)	Brake	Left Arrow or S
🤚 No Hand / Relaxed	Idle	No key pressed

🧠 How It Works:
The camera captures live video frames.
Every few frames (DETECTION_INTERVAL), MediaPipe detects the hand and its landmarks.
The script measures the vertical difference between:
INDEX_FINGER_TIP and INDEX_FINGER_PIP.
Based on that:
Tip above PIP → Accelerate
Tip below PIP → Brake
Close → Idle
Sends the corresponding keyboard input to your game.

🧰 Configuration:
Variable	Description	Default
USE_ARROW_KEYS	Use arrow keys instead of W/S	True
CAMERA_WIDTH, CAMERA_HEIGHT	Resolution for webcam	640x480
DETECTION_INTERVAL	How often MediaPipe runs (lower = slower)	3
ACCELERATE_THRESHOLD	Sensitivity for open hand	-0.06
BRAKE_THRESHOLD	Sensitivity for closed hand	0.06

🪪 License:
This project is licensed under the MIT License — feel free to use and modify it.
