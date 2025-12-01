# ============================================================================
# IMPORTS - External libraries needed for utility functions
# ============================================================================
import os  # Operating system functions for file and folder operations
from datetime import datetime  # Gets current date and time


# ============================================================================
# FOLDER PATH DEFINITIONS - Where all project data is stored
# ============================================================================

# Get the absolute path to the project root folder (one level up from 'app')
# Example: C:\Users\Danny K\OneDrive\Desktop\AI-Project
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Main data folder where all project data is stored
# Example: C:\Users\Danny K\OneDrive\Desktop\AI-Project\data
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

# Folder containing registered face images (organized by person name)
# Example: C:\Users\Danny K\OneDrive\Desktop\AI-Project\data\dataset
DATASET_DIR = os.path.join(DATA_DIR, 'dataset')

# Folder containing trained AI model files
# Example: C:\Users\Danny K\OneDrive\Desktop\AI-Project\data\encodings
ENCODINGS_DIR = os.path.join(DATA_DIR, 'encodings')

# Folder containing attendance CSV files
# Example: C:\Users\Danny K\OneDrive\Desktop\AI-Project\data\attendance
ATTENDANCE_DIR = os.path.join(DATA_DIR, 'attendance')


# ============================================================================
# ENSURE DIRECTORIES FUNCTION - Creates folders if they don't exist
# ============================================================================
def ensure_directories():
    """
    This function checks if the required folders exist, and creates them
    if they don't. This prevents errors when the program tries to save files.
    
    The 'exist_ok=True' parameter means: if folder already exists, don't error.
    """
    # Create dataset folder (for face images)
    os.makedirs(DATASET_DIR, exist_ok=True)
    
    # Create encodings folder (for AI model files)
    os.makedirs(ENCODINGS_DIR, exist_ok=True)
    
    # Create attendance folder (for CSV attendance records)
    os.makedirs(ATTENDANCE_DIR, exist_ok=True)


# ============================================================================
# TIMESTAMP FUNCTION - Returns current date and time as a string
# ============================================================================
def timestamp():
    """
    Returns the current date and time in a file-friendly format.
    
    Format: YYYY-MM-DD_HH-MM-SS
    Example: 2025-12-01_14-30-45
    
    This is useful for creating unique filenames.
    """
    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


# ============================================================================
# TODAY'S DATE FUNCTION - Returns current date as a string
# ============================================================================
def todays_date():
    """
    Returns today's date in a simple format.
    
    Format: YYYY-MM-DD
    Example: 2025-12-01
    
    This is used for naming daily attendance files.
    """
    return datetime.now().strftime('%Y-%m-%d')


# ============================================================================
# TEST CODE - Runs only when this file is executed directly
# ============================================================================
if __name__ == '__main__':
    # Create all necessary folders
    ensure_directories()
    
    # Print confirmation message with folder paths
    print('Directories ensured:')
    print(DATASET_DIR)
    print(ENCODINGS_DIR)
    print(ATTENDANCE_DIR)