#!/usr/bin/env python3
"""
Simple ASL Letter Recognition - Command Line Version
This version runs without the web interface for testing
"""

import cv2
import numpy as np
from asl_classifier import ASLClassifier

def main():
    print("ASL Letter Recognition - Simple Version")
    print("Press 'q' to quit, 's' to save image")
    print("=" * 40)
    
    # Initialize classifier
    classifier = ASLClassifier()
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    print("Webcam opened successfully")
    print("Make ASL signs in front of the camera...")
    
    frame_count = 0
    
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
                frame = classifier.draw_landmarks(frame, hand_landmarks)
            
            # Add text overlay
            cv2.putText(frame, f"Letter: {letter}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Confidence: {confidence:.2f}", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "Press 'q' to quit", (10, 110),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Show frame
            cv2.imshow('ASL Recognition', frame)
            
            # Print to console every 30 frames (about 1 second)
            frame_count += 1
            if frame_count % 30 == 0 and letter != "None":
                print(f"Detected: {letter} (confidence: {confidence:.2f})")
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                # Save current frame
                filename = f"asl_frame_{letter}_{confidence:.2f}.jpg"
                cv2.imwrite(filename, frame)
                print(f"Saved frame as {filename}")
    
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Camera released")

if __name__ == "__main__":
    main() 