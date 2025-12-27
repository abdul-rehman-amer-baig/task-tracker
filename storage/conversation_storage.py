import os
from typing import List, Dict
from .json_storage import load_json_file, save_json_file

CONVERSATION_FILE = "conversation_history.json"


def load_conversation_history(file_path: str = CONVERSATION_FILE) -> List[Dict]:
    history = load_json_file(file_path, default=[])
    if isinstance(history, list):
        return history
    return []


def save_conversation_history(
    history: List[Dict], file_path: str = CONVERSATION_FILE
) -> None:
    save_json_file(history, file_path, indent=2)


def add_to_history(
    history: List[Dict],
    role: str,
    content: str,
) -> List[Dict]:
    history.append({"role": role, "content": content})

    system_messages = [msg for msg in history if msg.get("role") == "system"]
    other_messages = [msg for msg in history if msg.get("role") != "system"]

    history = system_messages + other_messages

    return history


def clear_conversation_history(file_path: str = CONVERSATION_FILE) -> None:
    if os.path.exists(file_path):
        os.remove(file_path)
