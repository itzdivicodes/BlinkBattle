import cv2
import mediapipe as mp
import numpy as np
import math

class BlinkDetector:
    def __init__(self):
        # Initialize MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        
        # Simplified eye landmark indices (most reliable points)
        # Left eye: outer corner, top, inner corner, bottom
        self.LEFT_EYE = [33, 159, 133, 145]
        # Right eye: outer corner, top, inner corner, bottom  
        self.RIGHT_EYE = [362, 386, 263, 374]
        
        # Alternative eye points for better detection
        self.LEFT_EYE_ALT = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE_ALT = [362, 385, 387, 263, 373, 380]
        
        # Blink detection parameters
        self.EAR_THRESHOLD = 0.25  # Start with standard threshold
        self.CONSECUTIVE_FRAMES = 2
        self.blink_counter = 0
        self.total_blinks = 0
        self.frame_count = 0
        
        # For debugging
        self.ear_values = []
        self.debug_mode = True
        
        # For preventing double counting
        self.blink_in_progress = False
        self.frames_since_blink = 0
        self.MIN_FRAMES_BETWEEN_BLINKS = 10  # Minimum frames between blinks
        
    def distance(self, point1, point2):
        """Calculate Euclidean distance between two points"""
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def get_eye_aspect_ratio(self, eye_landmarks):
        """Calculate Eye Aspect Ratio using simple distance formula"""
        try:
            # Convert landmarks to pixel coordinates
            points = []
            for landmark in eye_landmarks:
                points.append([landmark.x, landmark.y])
            
            if len(points) < 4:
                return 0.3
            
            # Calculate vertical distances (height)
            vertical_1 = self.distance(points[1], points[3])  # top to bottom
            
            # Calculate horizontal distance (width)
            horizontal = self.distance(points[0], points[2])  # left to right
            
            # Calculate EAR
            if horizontal > 0:
                ear = vertical_1 / horizontal
            else:
                ear = 0.3
                
            return ear
        except Exception as e:
            if self.debug_mode:
                print(f"EAR calculation error: {e}")
            return 0.3
    
    def detect_blink_clean(self, frame):
        """Clean blink detection with blink count and eye landmarks overlay"""
        self.frame_count += 1
        self.frames_since_blink += 1
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        blink_detected = False
        ear_value = 0.0
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmarks = face_landmarks.landmark
                h, w = frame.shape[:2]
                
                # Get eye landmarks
                left_eye_landmarks = [landmarks[i] for i in self.LEFT_EYE]
                right_eye_landmarks = [landmarks[i] for i in self.RIGHT_EYE]
                
                # Draw green eye landmarks to show eyelid movement
                for i in self.LEFT_EYE + self.RIGHT_EYE:
                    x = int(landmarks[i].x * w)
                    y = int(landmarks[i].y * h)
                    cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
                
                # Calculate EAR for both eyes
                left_ear = self.get_eye_aspect_ratio(left_eye_landmarks)
                right_ear = self.get_eye_aspect_ratio(right_eye_landmarks)
                avg_ear = (left_ear + right_ear) / 2.0
                ear_value = avg_ear
                
                # Blink detection without visual feedback
                if avg_ear < self.EAR_THRESHOLD and not self.blink_in_progress:
                    self.blink_counter += 1
                    
                    if self.blink_counter >= self.CONSECUTIVE_FRAMES:
                        # Only count as blink if enough time has passed since last blink
                        if self.frames_since_blink >= self.MIN_FRAMES_BETWEEN_BLINKS:
                            blink_detected = True
                            self.total_blinks += 1
                            self.blink_in_progress = True
                            self.frames_since_blink = 0
                        self.blink_counter = 0
                elif avg_ear >= self.EAR_THRESHOLD:
                    # Eyes are open again, reset blink state
                    self.blink_counter = 0
                    if self.blink_in_progress and self.frames_since_blink > 5:
                        self.blink_in_progress = False
        
        # Add blink count overlay in left corner
        cv2.putText(frame, f"Blinks: {self.total_blinks}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        return blink_detected, frame, ear_value
    
    def detect_blink_simple(self, frame):
        """Simple blink detection using basic eye closure"""
        self.frame_count += 1
        self.frames_since_blink += 1
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        blink_detected = False
        ear_value = 0.0
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmarks = face_landmarks.landmark
                h, w = frame.shape[:2]
                
                # Get left eye landmarks
                left_eye_landmarks = [landmarks[i] for i in self.LEFT_EYE]
                right_eye_landmarks = [landmarks[i] for i in self.RIGHT_EYE]
                
                # Calculate EAR for both eyes
                left_ear = self.get_eye_aspect_ratio(left_eye_landmarks)
                right_ear = self.get_eye_aspect_ratio(right_eye_landmarks)
                avg_ear = (left_ear + right_ear) / 2.0
                ear_value = avg_ear
                
                # Store EAR values for analysis
                self.ear_values.append(avg_ear)
                if len(self.ear_values) > 30:  # Keep last 30 values
                    self.ear_values.pop(0)
                
                # Debug output every 30 frames
                if self.debug_mode and self.frame_count % 30 == 0:
                    avg_recent_ear = sum(self.ear_values) / len(self.ear_values) if self.ear_values else 0
                    print(f"Frame {self.frame_count}: Current EAR = {avg_ear:.3f}, Average = {avg_recent_ear:.3f}, Threshold = {self.EAR_THRESHOLD}")
                
                # Draw eye landmarks
                for i in self.LEFT_EYE + self.RIGHT_EYE:
                    x = int(landmarks[i].x * w)
                    y = int(landmarks[i].y * h)
                    cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
                
                # Improved blink detection with anti-double-counting
                if avg_ear < self.EAR_THRESHOLD and not self.blink_in_progress:
                    self.blink_counter += 1
                    cv2.putText(frame, "POTENTIAL BLINK", (10, 200), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    
                    if self.debug_mode:
                        print(f"Potential blink: EAR = {avg_ear:.3f}, Counter = {self.blink_counter}")
                    
                    if self.blink_counter >= self.CONSECUTIVE_FRAMES:
                        # Only count as blink if enough time has passed since last blink
                        if self.frames_since_blink >= self.MIN_FRAMES_BETWEEN_BLINKS:
                            blink_detected = True
                            self.total_blinks += 1
                            self.blink_in_progress = True
                            self.frames_since_blink = 0
                            if self.debug_mode:
                                print(f"*** BLINK DETECTED! *** Total: {self.total_blinks}")
                        self.blink_counter = 0
                elif avg_ear >= self.EAR_THRESHOLD:
                    # Eyes are open again, reset blink state
                    self.blink_counter = 0
                    if self.blink_in_progress and self.frames_since_blink > 5:
                        self.blink_in_progress = False
                
                # Display information
                cv2.putText(frame, f"EAR: {avg_ear:.3f}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                cv2.putText(frame, f"Threshold: {self.EAR_THRESHOLD}", (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
                cv2.putText(frame, f"Blinks: {self.total_blinks}", (10, 90), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                cv2.putText(frame, f"Counter: {self.blink_counter}", (10, 120), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)
                
                # Visual EAR indicator
                bar_length = 200
                bar_x = 300
                bar_y = 30
                
                # Background bar
                cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_length, bar_y + 20), (100, 100, 100), -1)
                
                # EAR level bar
                ear_length = int((avg_ear / 0.4) * bar_length)
                color = (0, 255, 0) if avg_ear > self.EAR_THRESHOLD else (0, 0, 255)
                cv2.rectangle(frame, (bar_x, bar_y), (bar_x + ear_length, bar_y + 20), color, -1)
                
                # Threshold line
                threshold_x = bar_x + int((self.EAR_THRESHOLD / 0.4) * bar_length)
                cv2.line(frame, (threshold_x, bar_y - 5), (threshold_x, bar_y + 25), (255, 255, 255), 2)
                
        else:
            cv2.putText(frame, "NO FACE DETECTED", (10, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            if self.debug_mode and self.frame_count % 30 == 0:
                print("No face detected")
        
        return blink_detected, frame, ear_value
    
    def detect_blink(self, frame):
        """Main blink detection method"""
        return self.detect_blink_simple(frame)
    
    def reset_blink_counter(self):
        """Reset blink counters for new game"""
        self.blink_counter = 0
        self.total_blinks = 0
        self.ear_values = []
        self.frame_count = 0
        self.blink_in_progress = False
        self.frames_since_blink = 0
        if self.debug_mode:
            print("Blink detector reset")
    
    def set_threshold(self, threshold):
        """Set new EAR threshold"""
        self.EAR_THRESHOLD = threshold
        print(f"Threshold set to: {threshold}")
    
    def toggle_debug(self):
        """Toggle debug mode"""
        self.debug_mode = not self.debug_mode
        print(f"Debug mode: {'ON' if self.debug_mode else 'OFF'}")

def main():
    print("=== SIMPLE BLINK DETECTION TEST ===")
    blink_detector = BlinkDetector()
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    print("Controls:")
    print("- Q: Quit")
    print("- R: Reset counter") 
    print("- +: Increase threshold")
    print("- -: Decrease threshold")
    print("- D: Toggle debug mode")
    print(f"Starting threshold: {blink_detector.EAR_THRESHOLD}")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        blink_detected, processed_frame, ear_value = blink_detector.detect_blink_clean(frame)
        
        if blink_detected:
            print(f" BLINK! EAR: {ear_value:.3f}")
        
        cv2.imshow('Simple Blink Detection', processed_frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            blink_detector.reset_blink_counter()
        elif key == ord('+') or key == ord('='):
            new_threshold = min(0.5, blink_detector.EAR_THRESHOLD + 0.02)
            blink_detector.set_threshold(new_threshold)
        elif key == ord('-'):
            new_threshold = max(0.1, blink_detector.EAR_THRESHOLD - 0.02)
            blink_detector.set_threshold(new_threshold)
        elif key == ord('d'):
            blink_detector.toggle_debug()
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
