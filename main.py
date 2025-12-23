from cli import parse_args
from storage import load_json, save_json
from task_logic import (
    add_task,
    update_task,
    delete_task,
    mark_in_progress_task,
    mark_done_task,
    list_tasks,
)
from presentation import format_tasks_table
from model import Status

DATA_FILE = "tasks.json"


if __name__ == "__main__":
    args = parse_args()

    tasks = load_json(DATA_FILE)

    try:
        if args.command == "add":
            add_task(
                tasks,
                args.task,
                save_fn=lambda t: save_json(t, DATA_FILE),
            )
            print("Task added successfully.")
            print(format_tasks_table(tasks))

        elif args.command == "update":
            update_task(
                tasks,
                args.id,
                args.task,
                save_fn=lambda t: save_json(t, DATA_FILE),
            )
            print("Task updated successfully.")
            print(format_tasks_table(tasks))
        elif args.command == "mark-in-progress":
            mark_in_progress_task(
                tasks,
                args.id,
                save_fn=lambda t: save_json(t, DATA_FILE),
            )
            print("Task marked as IN_PROGRESS.")
            print(format_tasks_table(tasks))
        elif args.command == "mark-done":
            mark_done_task(
                tasks,
                args.id,
                save_fn=lambda t: save_json(t, DATA_FILE),
            )
            print("Task marked as DONE.")
            print(format_tasks_table(tasks))
        elif args.command == "delete":
            delete_task(
                tasks,
                args.id,
                save_fn=lambda t: save_json(t, DATA_FILE),
            )
            print(f"Task deleted (ID: {args.id}).")
            print(format_tasks_table(tasks))
        elif args.command == "list":
            filtered_tasks = list_tasks(
                tasks,
                status=args.status if args.status else Status.TODO,
            )
            print(format_tasks_table(filtered_tasks))

    except ValueError as e:
        print(f"Error: {e}")
