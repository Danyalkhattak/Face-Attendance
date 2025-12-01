# ============================================================================
# IMPORTS - External libraries needed for face recognition and attendance
# ============================================================================
import cv2  # OpenCV - computer vision library for camera and face detection
import pickle  # Loads saved Python objects from files
import os  # Operating system functions for file operations
import sys  # System-specific parameters
from datetime import datetime  # Gets current date and time

# Add parent directory to path so we can import from 'app' folder
if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import our custom utility functions and folder paths
from app.utils import ENCODINGS_DIR, ATTENDANCE_DIR, todays_date


# ============================================================================
# MARK ATTENDANCE FUNCTION - Saves attendance records to a CSV file
# ============================================================================
def mark_attendance(names):
    """
    This function saves the names of recognized people to a CSV file
    with the current date and time.
    
    Parameters (inputs):
    - names: A list of names of people who were recognized
    
    CSV = Comma-Separated Values (a simple spreadsheet file that Excel can open)
    """
    
    # Get today's date in format: YYYY-MM-DD (example: 2025-12-01)
    today = todays_date()
    
    # Create the filename for today's attendance file
    # Example: 'data/attendance/attendance_2025-12-01.csv'
    attendance_file = os.path.join(ATTENDANCE_DIR, f'attendance_{today}.csv')
    
    # ========================================================================
    # CREATE FILE HEADER IF FILE DOESN'T EXIST
    # ========================================================================
    # Check if the file already exists
    if not os.path.exists(attendance_file):
        # If file doesn't exist, create it and write the header row
        with open(attendance_file, 'w') as f:
            f.write('Name,Time\n')  # Column headers
    
    # ========================================================================
    # APPEND ATTENDANCE RECORDS
    # ========================================================================
    # Open file in append mode (adds to end without deleting existing data)
    with open(attendance_file, 'a') as f:
        # Get current time in format: HH:MM:SS (example: 14:30:45)
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        # Write each person's name and timestamp to the file
        for name in names:
            f.write(f'{name},{timestamp}\n')  # Example: John_Doe,14:30:45
    
    # Print confirmation message
    print(f'[INFO] Attendance saved to {attendance_file}')


# ============================================================================
# RECOGNIZE AND MARK FUNCTION - Main attendance marking function
# ============================================================================
def recognize_and_mark(camera_index=0):
    """
    This function opens the camera, recognizes faces in real-time,
    and marks attendance for recognized people.
    
    Parameters (inputs):
    - camera_index: Which camera to use (0 = default webcam)
    """
    
    # ========================================================================
    # LOAD TRAINED MODEL AND NAME MAPPINGS
    # ========================================================================
    # Get paths to the saved model files
    model_path = os.path.join(ENCODINGS_DIR, 'face_model.yml')
    name_map_path = os.path.join(ENCODINGS_DIR, 'name_map.pickle')
    
    # Check if model files exist (user must train model first)
    if not os.path.exists(model_path) or not os.path.exists(name_map_path):
        print('[ERROR] Model not found! Please train the model first.')
        return
    
    # Load the trained face recognizer from file
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read(model_path)
    
    # Load the Haar Cascade face detector
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    
    # Load the name mappings (ID numbers to names)
    with open(name_map_path, 'rb') as f:
        name_data = pickle.load(f)
    id_to_name = name_data['id_to_name']  # Dictionary: {0: 'John_Doe', 1: 'Jane_Smith'}
    
    # ========================================================================
    # OPEN CAMERA
    # ========================================================================
    # Start capturing video from the webcam
    cap = cv2.VideoCapture(camera_index)
    
    # List to store names of people whose attendance has been marked
    # We use this to avoid marking the same person multiple times
    attendance = []
    
    # Print instructions
    print('[INFO] Starting recognition. Press Q to stop.')
    
    # ========================================================================
    # MAIN RECOGNITION LOOP - Process video frames continuously
    # ========================================================================
    while True:
        # Read one frame (image) from the camera
        ret, frame = cap.read()
        
        # If reading failed, stop the loop
        if not ret:
            break
        
        # Convert frame to grayscale (face detection works better with grayscale)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect all faces in the current frame
        # Returns list of rectangles: [(x, y, width, height), ...]
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # ====================================================================
        # PROCESS EACH DETECTED FACE
        # ====================================================================
        for (x, y, w, h) in faces:
            # Extract just the face region from grayscale image
            face_roi = gray[y:y+h, x:x+w]
            
            # Resize to standard size (must match training size)
            face_roi = cv2.resize(face_roi, (200, 200))
            
            # ================================================================
            # PREDICT WHO THIS FACE BELONGS TO
            # ================================================================
            # Ask the AI model to predict this person's ID
            # Returns: label (predicted ID number) and confidence (how sure it is)
            # Lower confidence = better match (it's actually a distance measure)
            label, confidence = face_recognizer.predict(face_roi)
            
            # ================================================================
            # DETERMINE IF PREDICTION IS CONFIDENT ENOUGH
            # ================================================================
            # IMPORTANT: LBPH confidence works as a distance metric
            # - Lower values = better match (more confident)
            # - Higher values = poor match (less confident)
            # Typical good matches: 30-80
            # Typical unknown faces: 100+
            
            # Adjusted threshold for better accuracy (was 100, now 70)
            # This helps distinguish between different people
            if confidence < 70:  # Threshold for accepting recognition (stricter now)
                # Look up the name from the predicted ID
                name = id_to_name.get(label, 'Unknown')
                
                # If person is recognized AND not already marked, add to attendance
                if name != 'Unknown' and name not in attendance:
                    attendance.append(name)  # Add to attendance list
                    print(f'[INFO] Marked: {name} (confidence: {confidence:.2f})')
            else:
                # If confidence is too high (poor match), mark as Unknown
                name = 'Unknown'
            
            # Debug: Print confidence for all faces (helps with tuning threshold)
            # Uncomment the line below if you want to see confidence values for tuning
            # print(f'[DEBUG] Face detected - Label: {label}, Name: {id_to_name.get(label, "Unknown")}, Confidence: {confidence:.2f}')
            
            # ================================================================
            # DRAW RECTANGLE AND NAME ON THE VIDEO
            # ================================================================
            # Choose color: Green for recognized, Red for unknown
            color = (0, 255, 0) if name != 'Unknown' else (0, 0, 255)
            
            # Draw rectangle around the face
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            # Draw text label above the rectangle showing name and confidence
            cv2.putText(
                frame,
                f'{name} ({confidence:.0f})',  # Text: "John_Doe (45)"
                (x, y-10),  # Position (slightly above rectangle)
                cv2.FONT_HERSHEY_SIMPLEX,  # Font style
                0.7,  # Font size
                color,  # Same color as rectangle
                2  # Thickness
            )
        
        # ====================================================================
        # SHOW VIDEO FRAME
        # ====================================================================
        # Display the video frame with rectangles and names drawn on it
        cv2.imshow('Attendance - Press Q to Quit', frame)
        
        # Wait 1 millisecond for key press; if 'Q' is pressed, exit loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # ========================================================================
    # CLEANUP - Release resources when done
    # ========================================================================
    # Release the camera
    cap.release()
    
    # Close all OpenCV windows
    cv2.destroyAllWindows()
    
    # ========================================================================
    # SAVE ATTENDANCE RECORDS
    # ========================================================================
    # If any faces were recognized, save their attendance
    if attendance:
        mark_attendance(attendance)
    else:
        # If no one was recognized, don't create a file
        print('[INFO] No faces recognized, no attendance saved')


# ============================================================================
# MAIN EXECUTION - Runs when this file is executed directly
# ============================================================================
if __name__ == '__main__':
    # Start the face recognition and attendance marking
    recognize_and_mark()