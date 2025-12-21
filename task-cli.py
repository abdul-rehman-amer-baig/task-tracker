import json
import os
import argparse
import enum


class Status(enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


def add_task(tasks, args):
    tasks.append(
        {
            "id": tasks[-1] + 1 if not tasks else 1,
            "task": args.task,
            "status": Status.TODO.value,
        }
    )

    save_json(tasks, DATA_FILE)

    print("Task added successfully")
    print(json.dumps(tasks[-1], indent=4))


def update_task(tasks, args):
    id_exists = False
    for i in range(len(tasks)):
        if tasks[i]["id"] == args.id:
            id_exists = True
            tasks[i]["task"] = args.task
            break

    if not id_exists:
        raise ValueError(f"Task with ID {args.id} not found")

    save_json(tasks, DATA_FILE)

    print("Task updated successfully")
    print(json.dumps(tasks[args.id], indent=4))


def delete_task(tasks, args):
    id_exists = False
    for i in range(len(tasks)):
        if tasks[i]["id"] == args.id:
            id_exists = True
            tasks.pop(i)
            break

    if not id_exists:
        raise ValueError(f"Task with ID {args.id} not found")

    save_json(tasks, DATA_FILE)
    print(f"Task deleted successfully (ID: {args.id})")


def mark_in_progress_task(tasks, args):
    id_exists = False
    for task in tasks:
        if task["id"] == args.id:
            task["status"] = Status.IN_PROGRESS.value
            id_exists = True
            break

    if not id_exists:
        raise ValueError(f"Task with ID {args.id} not found")

    save_json(tasks, DATA_FILE)

    print("Task marked as in progress successfully")
    print(json.dumps(task, indent=4))


def mark_done_task(tasks, args):
    id_exists = False
    for task in tasks:
        if task["id"] == args.id:
            task["status"] = Status.DONE.value
            id_exists = True
            break

    if not id_exists:
        raise ValueError(f"Task with ID {args.id} not found")

    save_json(tasks, DATA_FILE)

    print("Task marked as done successfully")
    print(json.dumps(task, indent=4))


def list_tasks(tasks, args):
    filtered_tasks = []
    if args.status == Status.DONE.value:
        filtered_tasks = [task for task in tasks if task["status"] == Status.DONE.value]
    elif args.status == Status.TODO.value:
        filtered_tasks = [task for task in tasks if task["status"] == Status.TODO.value]
    elif args.status == Status.IN_PROGRESS.value:
        filtered_tasks = [
            task for task in tasks if task["status"] == Status.IN_PROGRESS.value
        ]
    else:
        filtered_tasks = tasks

    print(json.dumps(filtered_tasks, indent=4))


def load_json(data_file):
    if not os.path.exists(data_file):
        with open(data_file, "w") as file:
            file.write("[]")
            return []
    else:
        with open(data_file, "r") as file:
            return json.load(file)


def save_json(tasks, data_file):
    with open(data_file, "w") as file:
        json.dump(tasks, file, indent=4)


def parse_args():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("task", type=str, help="The task to add")

    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, help="The id of the task to update")
    update_parser.add_argument("task", type=str, help="The task to update")

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="The id of the task to delete")

    mark_in_progress_parser = subparsers.add_parser(
        "mark-in-progress", help="Mark a task as in progress"
    )
    mark_in_progress_parser.add_argument(
        "id", type=int, help="The id of the task to mark as in progress"
    )

    mark_done_parser = subparsers.add_parser("mark-done", help="Mark a task as done")
    mark_done_parser.add_argument(
        "id", type=int, help="The id of the task to mark as done"
    )

    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(
        "status",
        nargs="?",
        choices=[Status.TODO.value, Status.IN_PROGRESS.value, Status.DONE.value],
        help="Filter tasks by status (TODO, IN_PROGRESS, DONE)",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    DATA_FILE = "tasks.json"
    tasks = load_json(DATA_FILE)

    command_map = {
        "add": add_task,
        "update": update_task,
        "delete": delete_task,
        "mark-in-progress": mark_in_progress_task,
        "mark-done": mark_done_task,
        "list": list_tasks,
    }

    command_map[args.command](tasks, args)
