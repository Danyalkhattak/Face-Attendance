# ============================================================================
# CAMERA UTILITY MODULE - Helper functions for camera operations
# ============================================================================
# This file contains reusable functions for opening and closing the webcam

import cv2  # OpenCV - library for working with camera and video


# ============================================================================
# OPEN CAMERA FUNCTION - Initializes and configures the webcam
# ============================================================================
def open_camera(camera_index=0, width=None, height=None):
    """
    Opens the webcam and optionally sets the resolution (image size).
    
    Parameters (inputs):
    - camera_index: Which camera to use (0 = default/built-in webcam)
    - width: Optional - desired video width in pixels (e.g., 640, 1280)
    - height: Optional - desired video height in pixels (e.g., 480, 720)
    
    Returns:
    - cap: A VideoCapture object that provides access to the camera
    
    Example usage:
        camera = open_camera(0, 640, 480)  # Opens default camera at 640x480
    """
    
    # Create a VideoCapture object connected to the specified camera
    cap = cv2.VideoCapture(camera_index)
    
    # If width is specified, set the camera's frame width
    if width:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    
    # If height is specified, set the camera's frame height
    if height:
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    # Return the camera object so other code can use it
    return cap


# ============================================================================
# RELEASE CAMERA FUNCTION - Properly closes the webcam
# ============================================================================
def release_camera(cap):
    """
    Safely releases the camera and closes all OpenCV windows.
    This frees up the camera so other programs can use it.
    
    Parameters (inputs):
    - cap: The VideoCapture object (camera) to release
    
    It's important to always release the camera when done, otherwise
    it might stay locked and unavailable for other applications.
    """
    
    try:
        # Release the camera (disconnect from it)
        cap.release()
    except Exception:
        # If releasing fails for any reason, just continue
        # (This prevents the program from crashing if camera is already released)
        pass
    
    # Close all OpenCV windows that might be open
    # This ensures no camera preview windows are left open
    cv2.destroyAllWindows()