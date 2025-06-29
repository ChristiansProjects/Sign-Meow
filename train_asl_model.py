#!/usr/bin/env python3
"""
ASL Model Training Script
Trains a machine learning model on reference ASL images
"""

import cv2
import numpy as np
import mediapipe as mp
import os
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
from pathlib import Path

class ASLModelTrainer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            max_num_hands=1
        )
        # Use class_weight='balanced' to mitigate class-imbalance during training
        self.model = RandomForestClassifier(
            n_estimators=300,
            random_state=42,
            class_weight="balanced"
        )
        self.features = []
        self.labels = []
        
    def extract_landmarks(self, image_path):
        """Extract hand landmarks from an image"""
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                return None
                
            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Process with MediaPipe
            results = self.hands.process(rgb_image)
            
            if results.multi_hand_landmarks:
                # Get the first detected hand
                hand_landmarks = results.multi_hand_landmarks[0]
                
                # Extract all landmark coordinates
                landmarks = []
                for landmark in hand_landmarks.landmark:
                    landmarks.extend([landmark.x, landmark.y, landmark.z])
                
                return np.array(landmarks)
            else:
                return None
                
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return None
    
    def load_dataset(self, dataset_path):
        """Load and process all images from the dataset folder"""
        print(f"Loading dataset from: {dataset_path}")
        
        dataset_path = Path(dataset_path)
        if not dataset_path.exists():
            print(f"Error: Dataset path {dataset_path} does not exist")
            return False
        
        # Find all image files
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(dataset_path.rglob(f"*{ext}"))
            # On Windows the filesystem is case-insensitive; adding the upper-case
            # variant creates duplicates. To be safe we still query but we will
            # deduplicate the final list with a set.
            image_files.extend(dataset_path.rglob(f"*{ext.upper()}"))
        
        # Deduplicate while preserving order
        seen = set()
        unique_image_files = []
        for p in image_files:
            key = str(p).lower()  # case-insensitive
            if key not in seen:
                unique_image_files.append(p)
                seen.add(key)
        
        image_files = unique_image_files
        
        print(f"Found {len(image_files)} unique image files (after deduplication)")
        
        if len(image_files) == 0:
            print("No image files found!")
            return False
        
        # Process each image
        processed_count = 0
        for image_path in image_files:
            # Try to extract letter from filename or folder structure
            letter = self.extract_letter_from_path(image_path, dataset_path)
            
            if letter:
                landmarks = self.extract_landmarks(str(image_path))
                if landmarks is not None:
                    self.features.append(landmarks)
                    self.labels.append(letter)
                    processed_count += 1
                    
                    if processed_count % 10 == 0:
                        print(f"Processed {processed_count} images...")
        
        print(f"Successfully processed {processed_count} images")
        return processed_count > 0
    
    def extract_letter_from_path(self, image_path, dataset_root):
        """Extract ASL letter from image path based on directory structure or filename.

        Expected dataset structure examples:
        archive/\n ├─ A/\n │   ├─ img1.jpg\n │   └─ ...\n ├─ B/\n │   └─ ...
        or filenames like "A_123.jpg".
        """
        # Make everything lower-case for case-insensitive matching
        path_str = str(image_path).lower()

        # 1) Directory name immediately inside dataset root
        try:
            rel = Path(image_path).relative_to(dataset_root)
            first_part = rel.parts[0]
            if len(first_part) == 1 and first_part.isalpha():
                return first_part.upper()
        except Exception:
            pass

        # 2) Check filename prefix (e.g., "c_123.jpg" or "c123.jpg")
        basename = Path(image_path).stem  # without suffix
        if basename and basename[0].isalpha():
            return basename[0].upper()

        # 3) Search for pattern _<letter>_  or _<letter>.
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            if f'_{letter}_' in path_str or f'_{letter}.' in path_str:
                return letter.upper()

        # Unknown label → skip
        return None
    
    def train_model(self):
        """Train the machine learning model"""
        if len(self.features) == 0:
            print("No features to train on!")
            return False
        
        print(f"\nTraining model on {len(self.features)} samples...")
        
        # Convert to numpy arrays
        X = np.array(self.features)
        y = np.array(self.labels)
        
        # Split into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Evaluate the model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\nModel Accuracy: {accuracy:.3f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Show class distribution
        unique_labels, counts = np.unique(y, return_counts=True)
        print(f"\nClass distribution:")
        for label, count in zip(unique_labels, counts):
            print(f"  {label}: {count}")
        
        return True
    
    def save_model(self, model_path="asl_model.pkl"):
        """Save the trained model"""
        model_data = {
            'model': self.model,
            'feature_names': [f'landmark_{i}' for i in range(len(self.features[0]))],
            'classes': list(self.model.classes_)
        }
        
        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"Model saved to: {model_path}")
    
    def load_model(self, model_path="asl_model.pkl"):
        """Load a trained model"""
        try:
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.model = model_data['model']
            print(f"Model loaded from: {model_path}")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False

def main():
    print("ASL Model Training")
    print("=" * 40)
    
    # Initialize trainer
    trainer = ASLModelTrainer()
    
    # Dataset path
    dataset_path = r"C:\Users\chris\Downloads\archive"
    
    # Load dataset
    if not trainer.load_dataset(dataset_path):
        print("Failed to load dataset!")
        return
    
    # Train model
    if not trainer.train_model():
        print("Failed to train model!")
        return
    
    # Save model
    trainer.save_model()
    
    print("\nTraining completed!")
    print("You can now use the trained model with the recognition script.")

if __name__ == "__main__":
    main() 