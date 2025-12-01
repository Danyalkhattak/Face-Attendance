# ============================================================================
# BUILD SCRIPT - Compiles the application to a standalone EXE file
# ============================================================================
# This script uses PyInstaller to create a Windows executable (.exe) file
# that can run on any Windows computer without needing Python installed.

"""
INSTRUCTIONS FOR BUILDING EXE:

1. First, install PyInstaller:
   Open PowerShell in this folder and run:
   pip install pyinstaller

2. Run this build script:
   python build_exe.py

3. Wait for the build to complete (may take 2-5 minutes)

4. Find your EXE in the 'dist' folder:
   dist/FaceAttendance/FaceAttendance.exe

5. The entire 'dist/FaceAttendance' folder can be copied to any Windows PC
   and will work without Python installed!
"""

import PyInstaller.__main__
import os

# ============================================================================
# BUILD CONFIGURATION
# ============================================================================

# Name of the output EXE file
app_name = "FaceAttendance"

# Main Python file to compile
main_file = "main.py"

# Additional data files to include (if any)
# Format: --add-data "source;destination"
data_files = [
    # If you have any config files or resources, add them here
    # Example: "--add-data", "config.json;.",
]

# Hidden imports (modules that PyInstaller might miss)
hidden_imports = [
    "cv2",
    "numpy",
    "customtkinter",
    "PIL",
    "imutils",
    "pickle",
]

# Build options
build_options = [
    main_file,  # Main script
    f"--name={app_name}",  # Name of the EXE
    "--onedir",  # Create a folder with EXE and dependencies (recommended)
    # Use "--onefile" instead of "--onedir" for single EXE (slower startup)
    "--windowed",  # No console window (GUI only)
    "--clean",  # Clean cache before building
    "--noconfirm",  # Overwrite output without asking
    
    # Icon (uncomment if you have an icon file)
    # "--icon=icon.ico",
    
    # Add hidden imports
    *[f"--hidden-import={imp}" for imp in hidden_imports],
    
    # Add data files
    *data_files,
]

# ============================================================================
# BUILD PROCESS
# ============================================================================

print("=" * 70)
print("🔨 BUILDING FACE ATTENDANCE SYSTEM EXE")
print("=" * 70)
print()
print("This may take 2-5 minutes. Please wait...")
print()

try:
    # Run PyInstaller with the specified options
    PyInstaller.__main__.run(build_options)
    
    print()
    print("=" * 70)
    print("✓ BUILD SUCCESSFUL!")
    print("=" * 70)
    print()
    print(f"Your executable is ready in: dist/{app_name}/")
    print()
    print("To use the application:")
    print(f"1. Go to the 'dist/{app_name}' folder")
    print(f"2. Run '{app_name}.exe'")
    print()
    print("To distribute:")
    print(f"- Copy the entire 'dist/{app_name}' folder to another PC")
    print("- Run the EXE from that folder")
    print("- The 'data' folder will be created automatically")
    print()
    
except Exception as e:
    print()
    print("=" * 70)
    print("✗ BUILD FAILED!")
    print("=" * 70)
    print()
    print(f"Error: {e}")
    print()
    print("Common solutions:")
    print("1. Make sure PyInstaller is installed: pip install pyinstaller")
    print("2. Make sure all dependencies are installed: pip install -r requirements.txt")
    print("3. Close the application if it's running")
    print("4. Delete 'build' and 'dist' folders and try again")
    print()
