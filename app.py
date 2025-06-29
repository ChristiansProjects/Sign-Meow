import cv2
import numpy as np
from flask import Flask, render_template, Response, jsonify
from flask_cors import CORS
from asl_classifier import ASLClassifier

app = Flask(__name__)
CORS(app)

# Initialize ASL classifier
classifier = ASLClassifier()

# Global variables
current_letter = "None"
confidence = 0.0

def process_frame(frame):
    """Process a single frame for ASL recognition"""
    global current_letter, confidence
    
    # Process frame with classifier
    letter, conf, hand_landmarks = classifier.process_frame(frame)
    
    # Update global variables
    current_letter = letter
    confidence = conf
    
    # Draw landmarks if hand detected
    if hand_landmarks:
        frame = classifier.draw_landmarks(frame, hand_landmarks)
    
    return frame

def generate_frames():
    """Generate video frames for streaming"""
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process frame for ASL recognition
            processed_frame = process_frame(frame)
            
            # Add text overlay
            cv2.putText(processed_frame, f"Letter: {current_letter}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(processed_frame, f"Confidence: {confidence:.2f}", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Add instructions
            cv2.putText(processed_frame, "Make ASL signs clearly", (10, 110),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Convert to JPEG
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            if not ret:
                continue
            
            frame_data = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
    
    finally:
        cap.release()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_letter')
def get_letter():
    """API endpoint to get current letter and confidence"""
    return jsonify({
        'letter': current_letter,
        'confidence': confidence
    })

if __name__ == '__main__':
    print("Starting ASL Recognition App...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 