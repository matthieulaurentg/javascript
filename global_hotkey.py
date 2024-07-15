import keyboard
import tkinter as tk
import win32gui
import win32con

class FullScreenApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-fullscreen', True)
        self.configure(bg='black')
        
        # Remove window border and title bar
        self.overrideredirect(True)
        
        # Set window to be topmost
        self.attributes('-topmost', True)
        
        # Create a label with instructions
        self.label = tk.Label(self, text="Press Esc to exit", fg="white", bg="black")
        self.label.pack(pady=20)
        
        # Hide the label after 2 seconds
        self.after(2000, self.label.pack_forget)
        
        # Bind Esc key to close the window
        self.bind('<Escape>', self.close)
        
        # Set focus to this window
        self.focus_force()
        
        # Hide the taskbar
        self.hide_taskbar()

    def hide_taskbar(self):
        taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
        win32gui.ShowWindow(taskbar, win32con.SW_HIDE)

    def show_taskbar(self):
        taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
        win32gui.ShowWindow(taskbar, win32con.SW_SHOW)

    def close(self, event=None):
        self.show_taskbar()
        self.destroy()

def create_black_screen():
    app = FullScreenApp()
    app.mainloop()

# Register the hotkey
keyboard.add_hotkey('ctrl+alt+p', create_black_screen)

print("Press Ctrl+Alt+P to open a fullscreen black screen.")
print("Press Ctrl+C in this console window to exit the script.")

# Keep the script running
keyboard.wait()