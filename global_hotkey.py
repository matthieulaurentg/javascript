import keyboard
import tkinter as tk
from tkinter import ttk

def create_black_screen():
    # Create the main window
    root = tk.Tk()
    root.title("Black Screen")
    
    # Make it fullscreen
    root.attributes('-fullscreen', True)
    
    # Set background to black
    root.configure(bg='black')
    
    # Create a label with instructions
    label = ttk.Label(root, text="Press Esc to exit", foreground="white", background="black")
    label.pack(pady=20)
    
    # Hide the label after 2 seconds
    root.after(2000, label.pack_forget)
    
    # Bind Esc key to close the window
    root.bind('<Escape>', lambda e: root.destroy())
    
    # Start the Tkinter event loop
    root.mainloop()

# Register the hotkey
keyboard.add_hotkey('ctrl+alt+p', create_black_screen)

print("Press Ctrl+Alt+P to open a fullscreen black screen.")
print("Press Ctrl+C in this console window to exit the script.")

# Keep the script running
keyboard.wait()