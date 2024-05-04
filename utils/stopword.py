from utils import config

def load(directory=config.STOP_WORD_URL):
    try:
        with open(directory, "r") as stop_file:
            return stop_file.read().split(",")
    except FileNotFoundError:
        print(f"Error: File '{directory}' not found.")
        return []

