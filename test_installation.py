#!/usr/bin/env python3
"""
Test script to verify ASL Recognition App installation
"""

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    
    try:
        print("Trying to import cv2...")
        import cv2
        print("✓ OpenCV imported successfully")
    except ImportError as e:
        print(f"✗ OpenCV import failed: {e}")
        return False
    
    try:
        print("Trying to import mediapipe...")
        import mediapipe as mp
        print("✓ MediaPipe imported successfully")
    except Exception as e:
        print(f"✗ MediaPipe import failed: {e}")
        return False
    
    try:
        print("Trying to import numpy...")
        import numpy as np
        print("✓ NumPy imported successfully")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False
    
    try:
        print("Trying to import flask...")
        from flask import Flask
        print("✓ Flask imported successfully")
    except ImportError as e:
        print(f"✗ Flask import failed: {e}")
        return False
    
    try:
        print("Trying to import flask_cors...")
        from flask_cors import CORS
        print("✓ Flask-CORS imported successfully")
    except ImportError as e:
        print(f"✗ Flask-CORS import failed: {e}")
        return False
    
    return True

def test_webcam():
    """Test if webcam can be accessed"""
    print("\nTesting webcam access...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("✗ Could not open webcam")
            return False
        
        ret, frame = cap.read()
        if not ret:
            print("✗ Could not read frame from webcam")
            cap.release()
            return False
        
        print(f"✓ Webcam working - Frame size: {frame.shape}")
        cap.release()
        return True
        
    except Exception as e:
        print(f"✗ Webcam test failed: {e}")
        return False

def test_mediapipe():
    """Test MediaPipe hand detection"""
    print("\nTesting MediaPipe hand detection...")
    
    try:
        import cv2
        import mediapipe as mp
        
        # Initialize MediaPipe
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        print("✓ MediaPipe hands model initialized successfully")
        hands.close()
        return True
        
    except Exception as e:
        print(f"✗ MediaPipe test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("ASL Recognition App - Installation Test")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import test failed. Please install missing packages:")
        print("pip install -r requirements.txt")
        return
    
    # Test webcam
    if not test_webcam():
        print("\n❌ Webcam test failed. Please check your webcam connection.")
        return
    
    # Test MediaPipe
    if not test_mediapipe():
        print("\n❌ MediaPipe test failed.")
        return
    
    print("\n✅ All tests passed! You can now run the ASL Recognition App:")
    print("python app.py")
    print("\nThen open your browser and go to: http://localhost:5000")

if __name__ == "__main__":
    main() 