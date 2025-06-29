#!/usr/bin/env python3
"""
Quick ASL Letter Recognition - Direct Camera Version
Opens camera immediately and recognizes ASL letters
"""

import cv2
import numpy as np
import mediapipe as mp

class QuickASLClassifier:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
            max_num_hands=1
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
    def is_finger_extended(self, landmarks, finger_tip_idx, finger_pip_idx):
        """Check if a finger is extended"""
        tip = landmarks[finger_tip_idx]
        pip = landmarks[finger_pip_idx]
        return tip.y < pip.y
    
    def classify_letter(self, landmarks):
        """Classify ASL letter based on finger states"""
        if not landmarks:
            return "None", 0.0
            
        # Get finger states
        thumb_extended = self.is_finger_extended(landmarks, 4, 3)
        index_extended = self.is_finger_extended(landmarks, 8, 6)
        middle_extended = self.is_finger_extended(landmarks, 12, 10)
        ring_extended = self.is_finger_extended(landmarks, 16, 14)
        pinky_extended = self.is_finger_extended(landmarks, 20, 18)
        
        # ASL letter classification
        if thumb_extended and not any([index_extended, middle_extended, ring_extended, pinky_extended]):
            return "A", 0.9
        elif all([index_extended, middle_extended, ring_extended, pinky_extended]) and not thumb_extended:
            return "B", 0.9
        elif index_extended and not any([middle_extended, ring_extended, pinky_extended, thumb_extended]):
            return "D", 0.9
        elif not any([index_extended, middle_extended, ring_extended, pinky_extended, thumb_extended]):
            return "E", 0.9
        elif index_extended and middle_extended and not any([ring_extended, pinky_extended, thumb_extended]):
            return "U", 0.9
        elif index_extended and middle_extended and ring_extended and not any([pinky_extended, thumb_extended]):
            return "W", 0.9
        elif pinky_extended and not any([index_extended, middle_extended, ring_extended, thumb_extended]):
            return "I", 0.9
        elif thumb_extended and pinky_extended and not any([index_extended, middle_extended, ring_extended]):
            return "Y", 0.9
        elif not any([index_extended, middle_extended, ring_extended, pinky_extended, thumb_extended]):
            return "S", 0.9
        else:
            return "None", 0.3
    
    def process_frame(self, frame):
        """Process a frame and return classification results"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            letter, confidence = self.classify_letter(hand_landmarks.landmark)
            return letter, confidence, hand_landmarks
        else:
            return "None", 0.0, None

def main():
    print("ASL Letter Recognition - Quick Start")
    print("Press 'q' to quit, 's' to save image")
    print("=" * 40)
    
    # Initialize classifier
    classifier = QuickASLClassifier()
    
    # Open camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    print("Camera opened successfully!")
    print("Make ASL signs in front of the camera...")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            
            # Process frame
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
            
            # Add text overlay
            cv2.putText(frame, f"Letter: {letter}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Confidence: {confidence:.2f}", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "Press 'q' to quit", (10, 110),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Show frame
            cv2.imshow('ASL Recognition', frame)
            
            # Print to console when letter detected
            if letter != "None":
                print(f"Detected: {letter} (confidence: {confidence:.2f})")
            
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

if __name__ == "__main__":
    main() 