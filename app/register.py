# ============================================================================
# IMPORTS - External libraries needed for face registration
# ============================================================================
import cv2  # OpenCV - library for working with camera and images
import os  # Operating system functions for file/folder operations
import sys  # System-specific parameters and functions

# Add parent directory to path so we can import from 'app' folder
# This is needed when running this file directly
if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import our custom utility functions
from app.utils import DATASET_DIR, ensure_directories


# ============================================================================
# REGISTER FACE FUNCTION - Captures photos of a person's face
# ============================================================================
def register_face(name: str, max_images=30, camera_index=0):
    """
    This function opens your webcam and lets you capture multiple photos
    of a person's face to register them in the system.
    
    Parameters (inputs):
    - name: The person's name (string/text)
    - max_images: How many photos to take (default is 30)
    - camera_index: Which camera to use (0 = default webcam)
    """
    
    # Make sure all required folders exist
    ensure_directories()
    
    # ========================================================================
    # PREPARE PERSON'S FOLDER
    # ========================================================================
    # Clean up the name: remove extra spaces and replace spaces with underscores
    # Example: "John Doe  " becomes "John_Doe"
    name = name.strip().replace(' ', '_')
    
    # Create a folder path for this person's images
    # Example: data/dataset/John_Doe/
    person_dir = os.path.join(DATASET_DIR, name)
    
    # Create the folder if it doesn't exist yet
    os.makedirs(person_dir, exist_ok=True)
    
    # ========================================================================
    # OPEN CAMERA
    # ========================================================================
    # Start capturing video from the webcam (camera_index 0 = default camera)
    cap = cv2.VideoCapture(camera_index)
    
    # Counter to track how many images we've captured
    count = 0
    
    # Print instructions to the user in the console
    print('[INFO] Press SPACE to capture an image. Press Q to quit early.')
    
    # ========================================================================
    # MAIN CAPTURE LOOP - Continuously show camera feed
    # ========================================================================
    while True:
        # Read one frame (image) from the camera
        ret, frame = cap.read()
        
        # If reading failed (camera problem), stop the loop
        if not ret:
            print('[ERROR] Failed to read from camera')
            break
        
        # Make a copy of the frame to display (so we don't modify original)
        display = frame.copy()
        
        # Get frame dimensions (height and width)
        h, w = display.shape[:2]
        
        # Add text overlay on the video showing progress
        # Parameters: image, text, position, font, size, color (green), thickness
        cv2.putText(
            display,
            f'Name: {name} - Images: {count}/{max_images}',  # Text to show
            (10, 30),  # Position (x=10, y=30 pixels from top-left)
            cv2.FONT_HERSHEY_SIMPLEX,  # Font style
            0.7,  # Font size
            (0, 255, 0),  # Color in BGR format (green)
            2  # Thickness of text
        )
        
        # Show the video frame in a window
        cv2.imshow('Register Face - Press SPACE to Capture / Q to Quit', display)
        
        # ====================================================================
        # KEYBOARD INPUT HANDLING
        # ====================================================================
        # Wait 1 millisecond for a key press
        key = cv2.waitKey(1) & 0xFF
        
        # If 'Q' key is pressed, quit early
        if key == ord('q'):
            break
        
        # If SPACE key is pressed (key code 32), capture an image
        elif key == 32:  # SPACE bar
            # Create file path for the image
            # Example: data/dataset/John_Doe/0.jpg, then 1.jpg, 2.jpg, etc.
            img_path = os.path.join(person_dir, f'{count}.jpg')
            
            # Save the current frame as an image file
            cv2.imwrite(img_path, frame)
            
            # Print confirmation message
            print(f'[INFO] Saved {img_path}')
            
            # Increase the counter
            count += 1
            
            # If we've reached the maximum number of images, stop
            if count >= max_images:
                print('[INFO] Reached max images')
                break
    
    # ========================================================================
    # CLEANUP - Release resources when done
    # ========================================================================
    # Release the camera so other programs can use it
    cap.release()
    
    # Close all OpenCV windows
    cv2.destroyAllWindows()
    
    # Print completion message
    print('[INFO] Registration finished')


# ============================================================================
# MAIN EXECUTION - Runs when this file is executed directly
# ============================================================================
if __name__ == '__main__':
    # Ask user to type the student's name in the console
    name = input('Enter student name: ').strip()
    
    # Check if name is empty (user didn't type anything)
    if not name:
        print('Name cannot be empty')
    else:
        # Start the face registration process
        register_face(name)