# 🎮 Hand Gesture Game Controller

A Python-based project that allows users to control games using hand gestures instead of a keyboard or mouse. The system uses computer vision to detect hand movements and converts them into game controls, providing a touch-free gaming experience.

---

## 📌 Project Overview

The Hand Gesture Game Controller captures live video from a webcam, detects hand landmarks using computer vision, and maps different gestures to keyboard actions. This enables users to play games such as Hill Climb Racing using only their hand movements.

---

## ✨ Features

- 🖐️ Real-time hand gesture detection
- 🎮 Control games using hand movements
- 📷 Webcam-based input
- ⚡ Fast and responsive gesture recognition
- 💻 Easy to set up and run

---

## 🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe
- PyAutoGUI / PyDirectInput
- Webcam

---

## 📂 Project Structure

```
handgestured_gamecontroller/
│── hillclimb_hand_control.py
│── package-lock.json
│── README.md
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/rahimulla322/handgestured_gamecontroller.git
```

### 2. Navigate to the project folder

```bash
cd handgestured_gamecontroller
```

### 3. Install the required Python packages

```bash
pip install opencv-python mediapipe pyautogui pydirectinput
```

---

## ▶️ Run the Project

```bash
python hillclimb_hand_control.py
```

Make sure your webcam is connected before running the program.

---

## 🎯 How It Works

1. Start the Python program.
2. The webcam captures your hand movements.
3. MediaPipe detects hand landmarks.
4. The program recognizes predefined gestures.
5. Corresponding keyboard inputs are sent to the game.
6. Play the game using only your hand gestures.

---

## 📸 Output

- Detects hand gestures in real time.
- Controls the game without touching the keyboard.
- Smooth and interactive gameplay.

---

## 🔮 Future Enhancements

- Support for multiple games
- Custom gesture mapping
- AI-based gesture recognition
- Multiplayer gesture support
- Mobile camera integration

---

## 👨‍💻 Author

**Rahim Ulla T C**

GitHub: https://github.com/rahimulla322

---

## 📄 License

This project is created for educational purposes.
