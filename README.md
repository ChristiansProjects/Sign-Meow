# ASL Letter Recognition App

A real-time American Sign Language (ASL) letter recognition application that uses computer vision to detect hand signs and translate them to English letters.

## Features

- Real-time webcam hand detection
- ASL letter recognition (A-Z)
- Modern web interface
- Live video feed with hand tracking
- Confidence scoring for predictions

## Setup Instructions

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your web browser and navigate to `http://localhost:5000`

## How it Works

The application uses:
- **MediaPipe** for hand landmark detection
- **OpenCV** for webcam input and image processing
- **TensorFlow** for the machine learning model
- **Flask** for the web interface

The system extracts hand landmarks from the webcam feed and uses a pre-trained model to classify the hand pose as an ASL letter.

## Usage

1. Position your hand in the webcam view
2. Make ASL letter signs clearly
3. The recognized letter will appear on screen
4. Hold the sign steady for best recognition

## Supported Letters

The app recognizes all 26 letters of the English alphabet in ASL format.

## Requirements

- Python 3.8+
- Webcam
- Good lighting conditions
- Clear hand positioning 