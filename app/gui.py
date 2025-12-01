# ============================================================================
# IMPORTS - These are external libraries we need for the program to work
# ============================================================================
import customtkinter as ctk  # Modern GUI library for beautiful interfaces
import os  # Helps us work with file paths and folders
import threading  # Allows running tasks in background without freezing GUI
from tkinter import messagebox, simpledialog  # Creates popup dialogs and input boxes
from app.utils import ensure_directories  # Our custom function to create needed folders
# Import the actual functions instead of running as subprocess
from app.register import register_face
from app.train import train_encodings
from app.attendance import recognize_and_mark


# ============================================================================
# MAIN GUI FUNCTION - This creates and runs the main application window
# ============================================================================
def run_gui():
    """
    This is the main function that creates the entire graphical user interface.
    It sets up the window, buttons, and all the visual elements you see.
    """
    
    # Create all necessary folders for the application (dataset, encodings, attendance)
    ensure_directories()
    
    # Set the app to use dark mode (modern look)
    ctk.set_appearance_mode('Dark')
    
    # Set the color theme - we're using a custom modern gradient theme
    ctk.set_default_color_theme('blue')
    
    # ========================================================================
    # MAIN WINDOW SETUP
    # ========================================================================
    # Create the main application window
    app = ctk.CTk()
    
    # Set the title that appears at the top of the window
    app.title('Face Recognition Attendance System')
    
    # Set window size: 900 pixels wide x 650 pixels tall
    app.geometry('900x650')
    
    # Prevent user from resizing the window (keeps design consistent)
    app.resizable(False, False)
    
    # ========================================================================
    # HEADER SECTION - The top banner with the title
    # ========================================================================
    # Create a header frame with gradient-like appearance
    header = ctk.CTkFrame(
        app,
        corner_radius=0,  # No rounded corners at top
        height=80,  # Header height in pixels
        fg_color=("#1e3a8a", "#1e40af")  # Gradient blue colors (light mode, dark mode)
    )
    header.pack(fill='x', pady=(0, 20))  # Fill entire width, add space below
    header.pack_propagate(False)  # Prevent header from shrinking
    
    # Create the main title text
    title = ctk.CTkLabel(
        header,
        text='🎓 Face Recognition Attendance System',  # Title with emoji
        font=('Segoe UI Bold', 28),  # Large bold font
        text_color='white'  # White text color
    )
    title.pack(expand=True)  # Center the title vertically
    
    # Create a subtitle/description text below the main title
    subtitle = ctk.CTkLabel(
        header,
        text='Advanced AI-Powered Student Attendance Management',
        font=('Segoe UI', 13),  # Smaller font
        text_color=('#e0e0e0', '#d0d0d0')  # Light gray color
    )
    subtitle.pack()
    
    # ========================================================================
    # MAIN CONTENT FRAME - The center card that holds all buttons
    # ========================================================================
    # Create the main container frame with modern rounded corners
    frame = ctk.CTkFrame(
        app,
        corner_radius=20,  # Smooth rounded corners (20 pixels radius)
        width=780,  # Width of the frame
        height=450,  # Height of the frame
        border_width=2,  # Thin border around the frame
        border_color=("#3b82f6", "#2563eb")  # Blue border color
    )
    frame.place(relx=0.5, rely=0.55, anchor='center')  # Center the frame in window
    frame.pack_propagate(False)  # Prevent frame from auto-resizing
    
    # ========================================================================
    # BUTTON FUNCTIONS - What happens when each button is clicked
    # ========================================================================
    
    def run_register():
        """
        This function runs when user clicks 'Register New Face' button.
        It opens a dialog to get the person's name, then opens camera to capture photos.
        Now everything happens in the GUI - no command-line needed!
        """
        # Show a custom input dialog to get the person's name
        dialog = ctk.CTkInputDialog(
            text="Enter the student's name:",
            title="Register New Face"
        )
        name = dialog.get_input()  # Wait for user to type name and click OK
        
        # Check if user entered a name (didn't click Cancel or leave it empty)
        if name and name.strip():
            # Show info message with instructions
            messagebox.showinfo(
                "📷 Ready to Capture",
                f"Camera will open for: {name}\n\n"
                "Instructions:\n"
                "• Press SPACE to capture each photo\n"
                "• Capture 20-30 photos from different angles\n"
                "• Press Q when finished\n\n"
                "Click OK to start..."
            )
            
            # Disable the button while capturing (prevent double-click)
            btn_register.configure(state="disabled", text="📷 Capturing...")
            
            # Run the registration in a separate thread so GUI doesn't freeze
            def register_thread():
                try:
                    # Call the register_face function with the entered name
                    register_face(name.strip())
                    # Show success message when done
                    app.after(0, lambda: messagebox.showinfo(
                        "✓ Success",
                        f"Registration complete for {name}!\n\n"
                        "Next step: Click 'Train AI Model' to teach\n"
                        "the system to recognize this face."
                    ))
                except Exception as e:
                    # Show error if something went wrong
                    app.after(0, lambda: messagebox.showerror(
                        "✗ Error",
                        f"Registration failed:\n{e}"
                    ))
                finally:
                    # Re-enable the button when done
                    app.after(0, lambda: btn_register.configure(
                        state="normal", 
                        text="📷 Register New Face"
                    ))
            
            # Start the registration thread
            threading.Thread(target=register_thread, daemon=True).start()
        else:
            # Show warning if name was empty
            messagebox.showwarning("⚠ Warning", "Name cannot be empty!")
    
    def run_train():
        """
        This function runs when user clicks 'Train Model' button.
        It processes all captured face images and teaches the AI to recognize them.
        Shows progress and completion messages in the GUI.
        """
        # Ask user to confirm they want to start training
        response = messagebox.askyesno(
            "🧠 Train AI Model",
            "This will train the AI model with all registered faces.\n\n"
            "Make sure you have registered at least one person.\n\n"
            "Training may take a few seconds to a few minutes\n"
            "depending on the number of images.\n\n"
            "Continue?"
        )
        
        if response:  # If user clicked Yes
            # Disable button during training
            btn_train.configure(state="disabled", text="🧠 Training...")
            
            # Run training in separate thread
            def train_thread():
                try:
                    # Call the train_encodings function
                    train_encodings()
                    # Show success message
                    app.after(0, lambda: messagebox.showinfo(
                        "✓ Success",
                        "Model training completed successfully!\n\n"
                        "The AI can now recognize registered faces.\n\n"
                        "Next step: Click 'Start Attendance' to\n"
                        "begin marking attendance."
                    ))
                except Exception as e:
                    # Show error message
                    app.after(0, lambda: messagebox.showerror(
                        "✗ Error",
                        f"Training failed:\n\n{str(e)}\n\n"
                        "Make sure you have registered at least\n"
                        "one person before training."
                    ))
                finally:
                    # Re-enable button
                    app.after(0, lambda: btn_train.configure(
                        state="normal",
                        text="🧠 Train AI Model"
                    ))
            
            # Start training thread
            threading.Thread(target=train_thread, daemon=True).start()
    
    def run_attendance():
        """
        This function runs when user clicks 'Start Attendance' button.
        It opens the camera and recognizes faces to mark attendance.
        Shows helpful instructions before starting.
        """
        # Show instructions before starting
        response = messagebox.askyesno(
            "✓ Start Attendance",
            "Camera will open for face recognition.\n\n"
            "Instructions:\n"
            "• Look at the camera\n"
            "• Green box = Recognized\n"
            "• Red box = Unknown\n"
            "• Press Q to finish and save\n\n"
            "Make sure you have trained the model first!\n\n"
            "Ready to start?"
        )
        
        if response:  # If user clicked Yes
            # Disable button during attendance marking
            btn_attendance.configure(state="disabled", text="✓ Marking...")
            
            # Run attendance in separate thread
            def attendance_thread():
                try:
                    # Call the recognize_and_mark function
                    recognize_and_mark()
                    # Show completion message
                    app.after(0, lambda: messagebox.showinfo(
                        "✓ Complete",
                        "Attendance marking finished!\n\n"
                        "Attendance has been saved to a CSV file.\n\n"
                        "Click 'View Attendance Records' to see the results."
                    ))
                except Exception as e:
                    # Show error message
                    app.after(0, lambda: messagebox.showerror(
                        "✗ Error",
                        f"Attendance marking failed:\n\n{str(e)}\n\n"
                        "Make sure the model is trained first."
                    ))
                finally:
                    # Re-enable button
                    app.after(0, lambda: btn_attendance.configure(
                        state="normal",
                        text="✓ Start Attendance"
                    ))
            
            # Start attendance thread
            threading.Thread(target=attendance_thread, daemon=True).start()
    
    def open_attendance_folder():
        """
        This function runs when user clicks 'View Records' button.
        It opens the folder where all attendance records (CSV files) are stored.
        """
        # Get the path to the attendance folder
        attendance_dir = os.path.join('data', 'attendance')
        
        # Check if the folder exists
        if os.path.exists(attendance_dir):
            # Check if there are any files in the folder
            files = os.listdir(attendance_dir)
            if files:
                # Open the folder in Windows Explorer
                os.startfile(attendance_dir)
            else:
                # Show message if folder is empty
                messagebox.showinfo(
                    "📊 No Records Yet",
                    "The attendance folder exists but is empty.\n\n"
                    "Mark attendance first to create records."
                )
        else:
            # Show warning if folder doesn't exist yet
            messagebox.showwarning(
                "⚠ Warning",
                "Attendance folder not found!\n\n"
                "No attendance records exist yet.\n\n"
                "Mark attendance first to create records."
            )
    
    # ========================================================================
    # BUTTONS - The four main action buttons with modern styling
    # ========================================================================
    
    # BUTTON 1: Register New Face
    # This button lets you add a new person to the system
    btn_register = ctk.CTkButton(
        frame,
        text='📷 Register New Face',  # Button text with camera emoji
        command=run_register,  # Function to call when clicked
        width=350,  # Button width
        height=60,  # Button height (taller for modern look)
        font=('Segoe UI Semibold', 16),  # Font style and size
        corner_radius=15,  # Very rounded corners
        fg_color=("#10b981", "#059669"),  # Green gradient color
        hover_color=("#059669", "#047857"),  # Darker green when mouse hovers over it
        border_width=0  # No border
    )
    btn_register.place(relx=0.5, rely=0.18, anchor='center')  # Position in frame
    
    # BUTTON 2: Train Model
    # This button trains the AI with all registered faces
    btn_train = ctk.CTkButton(
        frame,
        text='🧠 Train AI Model',  # Button text with brain emoji
        command=run_train,  # Function to call when clicked
        width=350,
        height=60,
        font=('Segoe UI Semibold', 16),
        corner_radius=15,
        fg_color=("#6366f1", "#4f46e5"),  # Purple/indigo gradient
        hover_color=("#4f46e5", "#4338ca"),  # Darker purple on hover
        border_width=0
    )
    btn_train.place(relx=0.5, rely=0.40, anchor='center')
    
    # BUTTON 3: Start Attendance
    # This button starts the face recognition to mark attendance
    btn_attendance = ctk.CTkButton(
        frame,
        text='✓ Start Attendance',  # Button text with checkmark emoji
        command=run_attendance,  # Function to call when clicked
        width=350,
        height=60,
        font=('Segoe UI Semibold', 16),
        corner_radius=15,
        fg_color=("#3b82f6", "#2563eb"),  # Blue gradient
        hover_color=("#2563eb", "#1d4ed8"),  # Darker blue on hover
        border_width=0
    )
    btn_attendance.place(relx=0.5, rely=0.62, anchor='center')
    
    # BUTTON 4: View Attendance Records
    # This button opens the folder with all attendance CSV files
    btn_view = ctk.CTkButton(
        frame,
        text='📊 View Attendance Records',  # Button text with chart emoji
        command=open_attendance_folder,  # Function to call when clicked
        width=350,
        height=60,
        font=('Segoe UI Semibold', 16),
        corner_radius=15,
        fg_color=("#f59e0b", "#d97706"),  # Orange/amber gradient
        hover_color=("#d97706", "#b45309"),  # Darker orange on hover
        border_width=0
    )
    btn_view.place(relx=0.5, rely=0.84, anchor='center')
    
    # ========================================================================
    # FOOTER - Small text at bottom of window
    # ========================================================================
    footer = ctk.CTkLabel(
        app,
        text='Made by Danny K, Musharib & Uzair  |  Version 1.0',
        font=('Segoe UI', 11),
        text_color=('#808080', '#a0a0a0')  # Gray color
    )
    footer.pack(side='bottom', pady=10)  # Place at bottom with padding
    
    # ========================================================================
    # START THE APPLICATION
    # ========================================================================
    # This line starts the GUI and keeps it running until user closes the window
    app.mainloop()
