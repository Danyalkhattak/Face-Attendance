# ============================================================================
# MAIN ENTRY POINT - This is where the program starts
# ============================================================================
# This is the main file that launches the Face Recognition Attendance System

# Import the function that creates and runs the graphical user interface (GUI)
from app.gui import run_gui


# ============================================================================
# PROGRAM EXECUTION
# ============================================================================
# The code below only runs when this file is executed directly
# (not when it's imported as a module in another file)
if __name__ == "__main__":
    # Start the graphical user interface
    # This opens the main window with all the buttons
    run_gui()