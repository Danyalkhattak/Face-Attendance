# ============================================================================
# IMPORTS - External libraries needed for training the AI model
# ============================================================================
import os  # Operating system functions for file operations
import pickle  # Saves and loads Python objects to/from files
from imutils import paths  # Utility to easily get all image file paths
import cv2  # OpenCV - computer vision library for face detection
import numpy as np  # NumPy - library for numerical operations and arrays
import sys  # System-specific parameters

# Add parent directory to path so we can import from 'app' folder
if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import our custom utility functions and folder paths
from app.utils import DATASET_DIR, ENCODINGS_DIR, ensure_directories


# ============================================================================
# TRAIN MODEL FUNCTION - Teaches the AI to recognize registered faces
# ============================================================================
def train_encodings():
    """
    This function trains the face recognition AI model using all the photos
    captured during registration. It goes through each image, detects faces,
    and teaches the AI to recognize them.
    
    Think of this like teaching a student: you show them many examples
    until they can recognize patterns on their own.
    """
    
    # Make sure all required folders exist
    ensure_directories()
    
    # ========================================================================
    # GET ALL IMAGES FROM DATASET
    # ========================================================================
    # Get a list of paths to all images in the dataset folder
    # Example: ['data/dataset/John_Doe/0.jpg', 'data/dataset/John_Doe/1.jpg', ...]
    imagePaths = list(paths.list_images(DATASET_DIR))
    
    # ========================================================================
    # INITIALIZE FACE DETECTION & RECOGNITION
    # ========================================================================
    # Load the Haar Cascade face detector (comes built-in with OpenCV)
    # This is a pre-trained model that can detect faces in images
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    
    # Create the LBPH (Local Binary Patterns Histograms) face recognizer
    # This is the AI algorithm that will learn to recognize different faces
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    # ========================================================================
    # PREPARE DATA STRUCTURES
    # ========================================================================
    # List to store all detected face images (as arrays of pixel values)
    faces = []
    
    # List to store labels (numbers) for each face
    # Example: John Doe = 0, Jane Smith = 1, Bob Johnson = 2
    labels = []
    
    # Dictionary to convert names to ID numbers
    # Example: {'John_Doe': 0, 'Jane_Smith': 1}
    name_to_id = {}
    
    # Dictionary to convert ID numbers back to names
    # Example: {0: 'John_Doe', 1: 'Jane_Smith'}
    id_to_name = {}
    
    # Counter for assigning unique IDs to each person
    current_id = 0
    
    # ========================================================================
    # PROCESS EACH IMAGE IN THE DATASET
    # ========================================================================
    print('[INFO] Starting training on dataset...')
    
    # Loop through each image file
    for (i, imagePath) in enumerate(imagePaths):
        # Show progress (which image we're processing)
        print(f'[INFO] Processing image {i+1}/{len(imagePaths)}: {imagePath}')
        
        # Extract the person's name from the folder path
        # Example: 'data/dataset/John_Doe/0.jpg' → 'John_Doe'
        name = imagePath.split(os.path.sep)[-2]
        
        # If this is a new person we haven't seen before, assign them a unique ID
        if name not in name_to_id:
            name_to_id[name] = current_id  # Assign current ID to this name
            id_to_name[current_id] = name  # Map ID back to name
            current_id += 1  # Increment ID for next new person
        
        # ====================================================================
        # READ AND PROCESS THE IMAGE
        # ====================================================================
        # Load the image from file
        image = cv2.imread(imagePath)
        
        # If image couldn't be loaded (corrupted file), skip it
        if image is None:
            print(f'[WARNING] Could not read {imagePath}. Skipping.')
            continue
        
        # Convert image to grayscale (black & white)
        # Face detection works better with grayscale images
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the image
        # Returns a list of rectangles (x, y, width, height) for each face found
        # Parameters: image, scale factor, min neighbors (for detection accuracy)
        detected_faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # ====================================================================
        # EXTRACT AND STORE EACH DETECTED FACE
        # ====================================================================
        # Loop through each face found in the image
        for (x, y, w, h) in detected_faces:
            # Extract just the face region from the grayscale image
            # [y:y+h, x:x+w] means: rows from y to y+h, columns from x to x+w
            face_roi = gray[y:y+h, x:x+w]
            
            # Resize the face to a standard size (200x200 pixels)
            # This ensures all faces have the same dimensions for training
            face_roi = cv2.resize(face_roi, (200, 200))
            
            # Add this face image to our training data
            faces.append(face_roi)
            
            # Add the corresponding label (person's ID number)
            labels.append(name_to_id[name])
    
    # ========================================================================
    # CHECK IF WE HAVE DATA TO TRAIN ON
    # ========================================================================
    # If no faces were detected in any images, we can't train
    if len(faces) == 0:
        print('[ERROR] No faces found in dataset!')
        return
    
    # ========================================================================
    # TRAIN THE AI MODEL
    # ========================================================================
    # Train the face recognizer using our collected faces and their labels
    # The AI learns patterns that distinguish different people's faces
    face_recognizer.train(faces, np.array(labels))
    
    # ========================================================================
    # SAVE THE TRAINED MODEL
    # ========================================================================
    # Create path for saving the model file
    model_path = os.path.join(ENCODINGS_DIR, 'face_model.yml')
    
    # Save the trained model to disk so we can use it later
    face_recognizer.save(model_path)
    
    # Create path for saving the name mappings
    name_map_path = os.path.join(ENCODINGS_DIR, 'name_map.pickle')
    
    # Save the name-to-ID and ID-to-name dictionaries
    # We'll need these to convert predictions back to names
    with open(name_map_path, 'wb') as f:
        pickle.dump({'id_to_name': id_to_name, 'name_to_id': name_to_id}, f)
    
    # ========================================================================
    # PRINT SUCCESS MESSAGE
    # ========================================================================
    print(f'[INFO] Training completed. Model saved to: {model_path}')
    print(f'[INFO] Trained on {len(faces)} faces from {len(name_to_id)} people')


# ============================================================================
# MAIN EXECUTION - Runs when this file is executed directly
# ============================================================================
if __name__ == '__main__':
    # Start the training process
    train_encodings()