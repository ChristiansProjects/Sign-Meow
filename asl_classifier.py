import numpy as np
import cv2
import mediapipe as mp

class ASLClassifier:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
            max_num_hands=1
        )
        
    def calculate_distance(self, point1, point2):
        """Calculate Euclidean distance between two points"""
        return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
    
    def is_finger_extended(self, landmarks, finger_tip_idx, finger_pip_idx, finger_mcp_idx):
        """Check if a finger is extended based on landmark positions"""
        tip = landmarks[finger_tip_idx]
        pip = landmarks[finger_pip_idx]
        mcp = landmarks[finger_mcp_idx]
        
        # Calculate distances
        tip_to_pip = self.calculate_distance(tip, pip)
        pip_to_mcp = self.calculate_distance(pip, mcp)
        
        # Finger is extended if tip is further from mcp than pip
        return tip_to_pip > pip_to_mcp * 0.8
    
    def get_finger_states(self, landmarks):
        """Get the extended state of all fingers"""
        if not landmarks:
            return None
            
        # MediaPipe hand landmark indices
        # Thumb: 4 (tip), 3 (pip), 2 (mcp)
        # Index: 8 (tip), 6 (pip), 5 (mcp)
        # Middle: 12 (tip), 10 (pip), 9 (mcp)
        # Ring: 16 (tip), 14 (pip), 13 (mcp)
        # Pinky: 20 (tip), 18 (pip), 17 (mcp)
        
        thumb_extended = self.is_finger_extended(landmarks, 4, 3, 2)
        index_extended = self.is_finger_extended(landmarks, 8, 6, 5)
        middle_extended = self.is_finger_extended(landmarks, 12, 10, 9)
        ring_extended = self.is_finger_extended(landmarks, 16, 14, 13)
        pinky_extended = self.is_finger_extended(landmarks, 20, 18, 17)
        
        return {
            'thumb': thumb_extended,
            'index': index_extended,
            'middle': middle_extended,
            'ring': ring_extended,
            'pinky': pinky_extended
        }
    
    def classify_letter(self, landmarks):
        """Classify ASL letter based on finger states"""
        if not landmarks:
            return "None", 0.0
            
        finger_states = self.get_finger_states(landmarks)
        if not finger_states:
            return "None", 0.0
            
        # Extract finger states
        thumb = finger_states['thumb']
        index = finger_states['index']
        middle = finger_states['middle']
        ring = finger_states['ring']
        pinky = finger_states['pinky']
        
        # ASL letter classification rules
        # A: Thumb extended, all other fingers closed
        if thumb and not any([index, middle, ring, pinky]):
            return "A", 0.9
            
        # B: All fingers extended, thumb closed
        elif all([index, middle, ring, pinky]) and not thumb:
            return "B", 0.9
            
        # C: All fingers curved (partially extended)
        elif not any([index, middle, ring, pinky, thumb]):
            # Check if fingers are partially extended
            return "C", 0.7
            
        # D: Only index finger extended
        elif index and not any([middle, ring, pinky, thumb]):
            return "D", 0.9
            
        # E: All fingers closed (fist)
        elif not any([index, middle, ring, pinky, thumb]):
            return "E", 0.9
            
        # F: Thumb and index finger touching (O shape with thumb)
        elif not any([middle, ring, pinky]) and thumb and index:
            return "F", 0.8
            
        # G: Index finger pointing to side
        elif index and not any([middle, ring, pinky, thumb]):
            return "G", 0.8
            
        # H: Index and middle finger pointing to side
        elif index and middle and not any([ring, pinky, thumb]):
            return "H", 0.8
            
        # I: Only pinky finger extended
        elif pinky and not any([index, middle, ring, thumb]):
            return "I", 0.9
            
        # J: Pinky finger extended (with motion - simplified)
        elif pinky and not any([index, middle, ring, thumb]):
            return "J", 0.8
            
        # K: Index and middle finger pointing up
        elif index and middle and not any([ring, pinky, thumb]):
            return "K", 0.9
            
        # L: Thumb and index finger forming L shape
        elif thumb and index and not any([middle, ring, pinky]):
            return "L", 0.9
            
        # M: Three fingers down (thumb, index, middle closed)
        elif not any([index, middle, thumb]) and any([ring, pinky]):
            return "M", 0.8
            
        # N: Two fingers down (thumb, index closed)
        elif not any([index, thumb]) and any([middle, ring, pinky]):
            return "N", 0.8
            
        # O: Fingers curled to form O shape
        elif not any([index, middle, ring, pinky, thumb]):
            return "O", 0.8
            
        # P: Index finger pointing down
        elif index and not any([middle, ring, pinky, thumb]):
            return "P", 0.7
            
        # Q: Index finger pointing down and to side
        elif index and not any([middle, ring, pinky, thumb]):
            return "Q", 0.7
            
        # R: Index and middle finger crossed
        elif index and middle and not any([ring, pinky, thumb]):
            return "R", 0.7
            
        # S: Fist (all fingers closed)
        elif not any([index, middle, ring, pinky, thumb]):
            return "S", 0.9
            
        # T: Thumb between index and middle finger
        elif thumb and not any([index, middle, ring, pinky]):
            return "T", 0.8
            
        # U: Index and middle finger pointing up
        elif index and middle and not any([ring, pinky, thumb]):
            return "U", 0.9
            
        # V: Index and middle finger pointing up (same as U)
        elif index and middle and not any([ring, pinky, thumb]):
            return "V", 0.9
            
        # W: Three fingers pointing up
        elif index and middle and ring and not any([pinky, thumb]):
            return "W", 0.9
            
        # X: Index finger bent
        elif not index and not any([middle, ring, pinky, thumb]):
            return "X", 0.7
            
        # Y: Thumb and pinky pointing up
        elif thumb and pinky and not any([index, middle, ring]):
            return "Y", 0.9
            
        # Z: Index finger drawing Z (simplified)
        elif index and not any([middle, ring, pinky, thumb]):
            return "Z", 0.6
            
        else:
            return "None", 0.3
    
    def process_frame(self, frame):
        """Process a frame and return classification results"""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process with MediaPipe
        results = self.hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            # Get the first detected hand
            hand_landmarks = results.multi_hand_landmarks[0]
            letter, confidence = self.classify_letter(hand_landmarks.landmark)
            return letter, confidence, hand_landmarks
        else:
            return "None", 0.0, None
    
    def draw_landmarks(self, frame, hand_landmarks):
        """Draw hand landmarks on the frame"""
        if hand_landmarks:
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing_styles = mp.solutions.drawing_styles
            
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )
        
        return frame 