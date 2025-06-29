#!/usr/bin/env python3
"""
Bridged ASL Recognition - Copy of trained_asl_recognition.py
"""

import cv2
import numpy as np
import mediapipe as mp
import pickle
import os
import threading
import queue
import serial
import time
try:
    import serial.tools.list_ports
except ImportError:
    serial = None
    print("Warning: pyserial is not installed. Serial bridge will be disabled.")

class TrainedASLClassifier:
    def __init__(self, model_path="asl_model.pkl"):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
            max_num_hands=1
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Load trained model
        self.model = None
        self.classes = []
        self.load_model(model_path)
        
    def load_model(self, model_path):
        """Load the trained machine learning model"""
        try:
            if os.path.exists(model_path):
                with open(model_path, 'rb') as f:
                    model_data = pickle.load(f)
                
                self.model = model_data['model']
                self.classes = model_data['classes']
                print(f"✓ Trained model loaded from {model_path}")
                print(f"✓ Supported letters: {', '.join(self.classes)}")
                return True
            else:
                print(f"✗ Model file {model_path} not found")
                print("Using fallback rule-based classification")
                return False
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            print("Using fallback rule-based classification")
            return False
    
    def extract_landmarks(self, landmarks):
        """Extract landmark features for prediction"""
        if not landmarks:
            return None
        
        # Extract all landmark coordinates
        features = []
        for landmark in landmarks.landmark:
            features.extend([landmark.x, landmark.y, landmark.z])
        
        return np.array(features).reshape(1, -1)
    
    def is_finger_extended(self, landmarks, finger_tip_idx, finger_pip_idx):
        """Check if a finger is extended (fallback method)"""
        tip = landmarks[finger_tip_idx]
        pip = landmarks[finger_pip_idx]
        return tip.y < pip.y
    
    def classify_letter_fallback(self, landmarks):
        """Fallback rule-based classification"""
        if not landmarks:
            return "None", 0.0
            
        # Get finger states
        thumb_extended = self.is_finger_extended(landmarks, 4, 3)
        index_extended = self.is_finger_extended(landmarks, 8, 6)
        middle_extended = self.is_finger_extended(landmarks, 12, 10)
        ring_extended = self.is_finger_extended(landmarks, 16, 14)
        pinky_extended = self.is_finger_extended(landmarks, 20, 18)
        
        # Enhanced ASL letter classification
        if thumb_extended and not any([index_extended, middle_extended, ring_extended, pinky_extended]):
            return "A", 0.8
        elif all([index_extended, middle_extended, ring_extended, pinky_extended]) and not thumb_extended:
            return "B", 0.8
        elif not any([index_extended, middle_extended, ring_extended, pinky_extended, thumb_extended]):
            # Check for C shape (curved fingers)
            return "C", 0.7
        elif index_extended and not any([middle_extended, ring_extended, pinky_extended, thumb_extended]):
            return "D", 0.8
        elif not any([index_extended, middle_extended, ring_extended, pinky_extended, thumb_extended]):
            return "E", 0.8
        elif index_extended and middle_extended and not any([ring_extended, pinky_extended, thumb_extended]):
            return "U", 0.8
        elif index_extended and middle_extended and ring_extended and not any([pinky_extended, thumb_extended]):
            return "W", 0.8
        elif pinky_extended and not any([index_extended, middle_extended, ring_extended, thumb_extended]):
            return "I", 0.8
        elif thumb_extended and pinky_extended and not any([index_extended, middle_extended, ring_extended]):
            return "Y", 0.8
        elif not any([index_extended, middle_extended, ring_extended, pinky_extended, thumb_extended]):
            return "S", 0.8
        else:
            return "None", 0.3
    
    def classify_letter(self, landmarks):
        """Classify ASL letter using trained model or fallback"""
        if not landmarks:
            return "None", 0.0
        # Try trained model first
        if self.model is not None:
            try:
                features = self.extract_landmarks(landmarks)
                if features is not None:
                    prediction = self.model.predict(features)[0]
                    confidence = np.max(self.model.predict_proba(features))
                    print(f"[MODEL] Predicted: {prediction} (confidence: {confidence:.2f})")
                    return prediction, confidence
            except Exception as e:
                print(f"Model prediction failed: {e}")
        # Fallback to rule-based classification
        letter, confidence = self.classify_letter_fallback(landmarks.landmark)
        print(f"[FALLBACK] Predicted: {letter} (confidence: {confidence:.2f})")
        return letter, confidence
    
    def process_frame(self, frame):
        """Process a frame and return classification results"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            letter, confidence = self.classify_letter(hand_landmarks)
            return letter, confidence, hand_landmarks
        else:
            return "None", 0.0, None

def find_esp32_port(preferred_port="COM5"):
    if serial is None:
        return None
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if preferred_port in port.device:
            return port.device
        if any(x in port.description for x in ["CP210", "CH340", "USB Serial", "Silicon"]):
            return port.device
    if ports:
        return ports[0].device
    return None

def serial_listener(ser, word_queue, done_queue):
    """Background thread to listen for ESP32 messages."""
    buffer = ""
    while True:
        try:
            data = ser.read(ser.in_waiting or 1).decode(errors='ignore')
            if data:
                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()
                    if line.startswith("WORD:"):
                        word = line[5:].strip().upper()
                        word_queue.put(word)
                    elif line == "DONE":
                        done_queue.put(True)
        except Exception as e:
            print(f"Serial listener error: {e}")
            break

def main():
    print("Bridged ASL Recognition - Enhanced Version")
    print("Press 'q' to quit, 's' to save image")
    print("=" * 50)
    
    # Serial setup for ESP32 bridge
    if serial is None:
        ser = None
        print("pyserial not available. Serial bridge disabled.")
    else:
        esp32_port = find_esp32_port()
        if esp32_port is None:
            print("ESP32 serial port not found! Please check connection.")
            ser = None
        else:
            try:
                print(f"Connecting to ESP32 on {esp32_port}...")
                ser = serial.Serial(esp32_port, 115200, timeout=1)
            except Exception as e:
                print(f"Failed to open serial port: {e}")
                ser = None
    
    # Queues for inter-thread communication
    word_queue = queue.Queue()
    done_queue = queue.Queue()
    # Start serial listener thread
    if ser:
        listener_thread = threading.Thread(target=serial_listener, args=(ser, word_queue, done_queue), daemon=True)
        listener_thread.start()
    
    # Initialize classifier
    classifier = TrainedASLClassifier()
    # Open camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    print("Camera opened successfully!")
    print("Make ASL signs in front of the camera...")
    current_word = None
    letter_index = 0
    try:
        while True:
            # Wait for a new word from ESP32
            if current_word is None:
                print("Waiting for word from ESP32...")
                current_word = word_queue.get().strip().upper()
                print(f"Spell this word: {current_word}")
                letter_index = 0
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            letter, confidence, hand_landmarks = classifier.process_frame(frame)
            # Draw landmarks if hand detected
            if hand_landmarks:
                classifier.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    classifier.mp_hands.HAND_CONNECTIONS,
                    classifier.mp_drawing_styles.get_default_hand_landmarks_style(),
                    classifier.mp_drawing_styles.get_default_hand_connections_style()
                )
            # Add overlays
            cv2.putText(frame, f"Word: {current_word}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            cv2.putText(frame, f"Next: {current_word[letter_index] if letter_index < len(current_word) else '-'}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Letter: {letter}", (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Confidence: {confidence:.2f}", (10, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Bridged ASL Recognition', frame)
            # Check for correct letter in sequence
            if (letter != "None" and
                letter_index < len(current_word) and
                letter == current_word[letter_index] and
                confidence > 0.4):
                print(f"Correct: {letter}")
                letter_index += 1
                if letter_index >= len(current_word):
                    print("Word completed! Triggering servo...")
                    if ser:
                        ser.write(b"SERVO\n")
                        ser.flush()
                        ser.write(b"LED_BLINK\n") 
                    # Wait for DONE from ESP32
                    done_queue.get()
                    print("Servo done. Waiting for next word...")
                    current_word = None
                    letter_index = 0
                    continue  # Wait for next word
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                filename = f"asl_{letter}_{confidence:.2f}.jpg"
                cv2.imwrite(filename, frame)
                print(f"Saved: {filename}")
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Camera released")
        if 'ser' in locals() and ser:
            try:
                ser.close()
                print("Serial port closed")
            except Exception:
                pass

if __name__ == "__main__":
    main() 