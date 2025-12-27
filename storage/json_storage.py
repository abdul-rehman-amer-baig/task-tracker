import json
import os
from typing import Any
from model import Task


def load_json_file(data_file: str, default: Any = None) -> Any:
    if default is None:
        default = []

    if not os.path.exists(data_file):
        with open(data_file, "w") as file:
            json.dump(default, file, indent=2)
        return default

    try:
        with open(data_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return default


def save_json_file(data: Any, data_file: str, indent: int = 2) -> None:
    try:
        with open(data_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=indent)
    except IOError as e:
        print(f"Warning: Could not save to {data_file}: {e}")


def load_json(data_file: str):
    tasks_data = load_json_file(data_file, default=[])
    return [Task(**task) for task in tasks_data]


def save_json(tasks, data_file: str):
    tasks_data = [task.model_dump() for task in tasks]
    save_json_file(tasks_data, data_file, indent=4)
