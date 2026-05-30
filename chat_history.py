import json
import os

CHAT_FILE = "chat_history.json"


# Load chat history
def load_chat_history():

    if os.path.exists(CHAT_FILE):

        with open(CHAT_FILE, "r") as file:
            return json.load(file)

    return []


# Save chat history
def save_chat_history(history):

    with open(CHAT_FILE, "w") as file:
        json.dump(history, file, indent=4)