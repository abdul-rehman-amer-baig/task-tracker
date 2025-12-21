import json
import os
from model import Task


def load_json(data_file):
    if not os.path.exists(data_file):
        with open(data_file, "w") as file:
            file.write("[]")
            return []
    else:
        with open(data_file, "r") as file:
            return [Task(**task) for task in json.load(file)]


def save_json(tasks, data_file):
    with open(data_file, "w") as file:
        json.dump([task.model_dump() for task in tasks], file, indent=4)
