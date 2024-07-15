import keyboard
import webbrowser
import time

def open_fullscreen_blackscreen():
    # Open the URL
    webbrowser.open('https://www.whitescreen.online/black-screen/')
    
    # Wait for the page to load (adjust the time if needed)
    time.sleep(2)
    
    # Simulate pressing F11 to enter fullscreen mode
    keyboard.press_and_release('f11')

# Set up the hotkey
keyboard.add_hotkey('ctrl+alt+p', open_fullscreen_blackscreen)

print("Press Ctrl+Alt+P to open the black screen in fullscreen mode.")
print("Press Ctrl+C to exit the script.")

# Keep the script running
keyboard.wait()