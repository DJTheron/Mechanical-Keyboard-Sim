import os
import subprocess
import threading
from pynput import keyboard
import random

sounds = ["enter.m4a", "space.m4a", "cmd.m4a", "key1.m4a", "key2.m4a", "key3.m4a", "key4.m4a", "key5.m4a", "key6.m4a", 
          "key7.m4a", "key8.m4a", "key9.m4a", "key10.m4a", "key11.m4a", "key12.m4a"]

def play_sound(file):
    # Resolve to an absolute path to avoid cwd issues
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, file)

    # Run afplay in a separate thread so key presses don't block
    try:
        subprocess.Popen(["afplay", file_path])
    except FileNotFoundError:
        print(f"Sound file not found: {file_path}")
    except Exception as exc:
        print(f"Failed to play {file_path}: {exc}")

def on_press(key):
    # Get the key that was pressed
    try:
        key_pressed = key.char  # For regular characters
    except AttributeError:
        key_pressed = key.name  # For special keys (shift, ctrl, etc.)
    
    if key_pressed == "enter":
        play_sound(sounds[0])

    elif key_pressed == "space":
        play_sound(sounds[1])

    elif key_pressed == "cmd":
        play_sound(sounds[2])   

    else:
        sound_file = random.choice([x for x in sounds if x not in (sounds[0], sounds[1], sounds[2])])
        play_sound(sound_file)


# Start the global keyboard listener
print("Keyboard sound simulator running... Press Ctrl+C to stop.")
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()