from cli import parse_args
from storage import load_json
from task_logic import (
    add_task,
    update_task,
    delete_task,
    mark_in_progress_task,
    mark_done_task,
    list_tasks,
)


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

    if args.command == "list":
        result = command_map[args.command](tasks, args)
    else:
        result = command_map[args.command](tasks, args, DATA_FILE)
        print(result)
