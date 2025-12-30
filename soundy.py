import subprocess
import threading
from pynput import keyboard

def play_sound(file):
    # Run afplay in a separate thread so key presses don't block
    subprocess.Popen(["afplay", file])

def on_press(key):
    play_sound("sound.mp3")

# Start the global keyboard listener
print("Keyboard sound simulator running... Press Ctrl+C to stop.")
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()