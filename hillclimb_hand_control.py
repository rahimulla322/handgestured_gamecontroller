import cv2
import mediapipe as mp
import pydirectinput
import keyboard
import time
import os

# --- Configuration ---
USE_ARROW_KEYS = True 

# --- Optimization Settings for Performance ---
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
DETECTION_INTERVAL = 3 # Process MediaPipe every 3 frames (Faster detection)
frame_counter = 0

# --- State Variables ---
# 0: Idle/No Hand, 1: Accelerate (Open), 2: Brake (Closed)
current_gesture_state = 0 
LAST_DETECTED_HAND_LABEL = "None" 

# --- MediaPipe Initialization (Optimized) ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6, # Slightly increased confidence for robustness
    min_tracking_confidence=0.5) 
mp_drawing = mp.solutions.drawing_utils 

# --- Key Mapping ---
# Note: For typical driving games, 'w' or 'up' is Accelerate, and 's' or 'down' is Brake.
# Based on your original code, we'll keep the key mapping for your specific setup.
GAS_KEY = 'right' if USE_ARROW_KEYS else 'w'
BRAKE_KEY = 'left' if USE_ARROW_KEYS else 's'

# --- Control & Gesture Functions ---
def accelerate():
    pydirectinput.keyDown(GAS_KEY)
    pydirectinput.keyUp(BRAKE_KEY)

def brake():
    pydirectinput.keyDown(BRAKE_KEY)
    pydirectinput.keyUp(GAS_KEY)

def release_controls():
    pydirectinput.keyUp(GAS_KEY)
    pydirectinput.keyUp(BRAKE_KEY)

# 🚀 CORRECTED Gesture Logic Function
def determine_hand_gesture(landmarks):
    """
    Determines the gesture: 1 for Accelerate, 2 for Brake, 0 for Idle.
    Uses the vertical difference between the Index finger tip (y) and PIP joint (y).
    """
    
    # Get the Y-coordinates of the Index finger landmarks
    # Y=0 is the top, Y=1 is the bottom of the frame.
    tip_y = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    pip_y = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
    
    # Calculate the vertical difference: tip_y - pip_y
    # Tip is HIGHER (Open): vertical_diff is negative (tip_y < pip_y)
    # Tip is LOWER (Closed): vertical_diff is positive (tip_y > pip_y)
    vertical_diff = tip_y - pip_y 
    
    # Define normalized distance thresholds (adjust these values for sensitivity)
    # Tighter thresholds (e.g., 0.03) are more sensitive; wider thresholds (e.g., 0.08) are less.
    # Set to a stable value of 0.06 (6% of frame height)
    ACCELERATE_THRESHOLD = -0.06 
    BRAKE_THRESHOLD = 0.06      

    # 1. Accelerate (Fully Open): Tip is significantly above PIP
    if vertical_diff < ACCELERATE_THRESHOLD: 
        return 1 # Accelerate 

    # 2. Brake (Fully Closed): Tip is significantly below PIP
    elif vertical_diff > BRAKE_THRESHOLD: 
        return 2 # Brake 

    # 3. Idle (Dead Zone): Tip is close to PIP (relaxed/partial curl)
    else:
        return 0 # Idle


# --- Main Video Processing Loop ---
if __name__ == "__main__":
    
    # Try common camera indices
    cap = cv2.VideoCapture(1) 
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        if not cap.isOpened():
            print("CRITICAL ERROR: Could not open video stream. Check your webcam connection.")
            release_controls() 
            os._exit(1) 

    print("--- Hand Controller Running (Requires Right Hand) ---")
    print(f"Controls: ACCELERATE='{GAS_KEY}', BRAKE='{BRAKE_KEY}'")
    
    time.sleep(2) 

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_counter += 1
        
        frame = cv2.flip(frame, 1) # Flip the frame for a 'mirror' view
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Conditional Processing for Optimization (MediaPipe runs only every N frames)
        process_current_frame = (frame_counter % DETECTION_INTERVAL == 0)
        
        results = None
        if process_current_frame:
            rgb_frame.flags.writeable = False 
            results = hands.process(rgb_frame)
            rgb_frame.flags.writeable = True
            frame_counter = 0 
            
            # --- Gesture Detection and State Update ---
            new_gesture = 0 # Default to Idle/No Hand
            LAST_DETECTED_HAND_LABEL = "None"
            
            if results.multi_hand_landmarks and results.multi_handedness:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    hand_label = handedness.classification[0].label
                    
                    if hand_label == 'Right':
                        LAST_DETECTED_HAND_LABEL = "Right"
                        
                        # 🟢 Call the updated gesture function
                        new_gesture = determine_hand_gesture(hand_landmarks)
                        
                        # Draw landmarks for the detected 'Right' hand
                        mp_drawing.draw_landmarks(
                            frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                            mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                        )
                        break 
                        
            # Update the persistent state
            current_gesture_state = new_gesture
        
        # --- Execute Controls and Display Status (Runs on ALL frames) ---
        
        control_text = "IDLE"
        text_color = (255, 255, 0) # Yellow for Idle
        
        if current_gesture_state == 2: # Brake (Fully Closed)
            brake()
            control_text = "BRAKE"
            text_color = (0, 0, 255) # Red for Brake
        
        elif current_gesture_state == 1: # Accelerate (Fully Open)
            accelerate()
            control_text = "ACCELERATE"
            text_color = (0, 255, 0) # Green for Accelerate
        
        else: # Idle (Dead Zone or No Hand)
            release_controls()
            if LAST_DETECTED_HAND_LABEL == "Right":
                 control_text = "IDLE (Dead Zone)"
            else:
                 control_text = "IDLE (No Hand)"

        cv2.putText(frame, control_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv2.LINE_AA)
        
        # Status line
        status_text = f"Hand: {LAST_DETECTED_HAND_LABEL} | Control: {control_text} | Processing: {'Tracking' if not process_current_frame else 'Detecting'}"
        cv2.putText(frame, status_text, (10, CAMERA_HEIGHT - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1, cv2.LINE_AA)

        # --- Display the live webcam feed ---
        cv2.imshow('Hand Controller View', frame)

        # --- Exit Check ---
        if cv2.waitKey(1) & 0xFF == ord('q') or keyboard.is_pressed('q'):
            break

    # --- Cleanup ---
    release_controls() 
    cap.release()
    cv2.destroyAllWindows()
    print("--- Control Program Ended ---")