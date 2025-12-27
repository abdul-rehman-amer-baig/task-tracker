import os
from dotenv import load_dotenv
from cli import parse_args
from storage import (
    load_json,
    save_json,
    load_conversation_history,
    save_conversation_history,
    add_to_history,
)
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
from ai.parser import parse_human_input

load_dotenv()

DATA_FILE = "tasks.json"


def execute_command(command_dict, tasks, data_file):
    message = command_dict.get("message")
    if message:
        print(message)

    cmd = command_dict.get("command")
    task_id = command_dict.get("id")
    task_text = command_dict.get("task")
    status_raw = command_dict.get("status")

    if status_raw is None:
        status = None
    elif isinstance(status_raw, str):
        status = getattr(Status, status_raw.upper(), None)
    else:
        status = status_raw

    if cmd == "add":
        add_task(tasks, task_text, save_fn=lambda t: save_json(t, data_file))
        print("Task added successfully.")
    elif cmd == "update":
        update_task(
            tasks, task_id, task_text, save_fn=lambda t: save_json(t, data_file)
        )
        print("Task updated successfully.")
    elif cmd == "mark-done":
        mark_done_task(tasks, task_id, save_fn=lambda t: save_json(t, data_file))
        print(f"Task marked as DONE (ID: {task_id})")
    elif cmd == "mark-in-progress":
        mark_in_progress_task(tasks, task_id, save_fn=lambda t: save_json(t, data_file))
        print(f"Task marked as IN_PROGRESS (ID: {task_id})")
    elif cmd == "delete":
        delete_task(tasks, task_id, save_fn=lambda t: save_json(t, data_file))
        print(f"Task deleted (ID: {task_id})")
    elif cmd == "list":
        filtered_tasks = list_tasks(tasks, status=status)
        print(format_tasks_table(filtered_tasks))
    else:
        print("Command not recognized.")


if __name__ == "__main__":
    args = parse_args()
    tasks = load_json(DATA_FILE)

    try:
        if args.command == "ai":
            history_enabled = os.getenv("ENABLE_CONVERSATION_HISTORY", True)

            conversation_history = None
            if history_enabled:
                conversation_history = load_conversation_history()

            response = parse_human_input(
                args.text, tasks, conversation_history=conversation_history
            )

            if response.get("type") == "conversation":
                message = response.get("message", "I'm here to help with your tasks!")
                print(message)
                if history_enabled:
                    conversation_history = add_to_history(
                        conversation_history, "user", args.text
                    )
                    conversation_history = add_to_history(
                        conversation_history, "assistant", message
                    )
                    save_conversation_history(conversation_history)
            else:
                if response.get("type") == "command":
                    command_dict = response
                else:
                    command_dict = response

                execute_command(command_dict, tasks, DATA_FILE)

                if history_enabled:
                    conversation_history = add_to_history(
                        conversation_history, "user", args.text
                    )
                    save_conversation_history(conversation_history)
        else:
            command_dict = {
                "command": args.command,
                "id": getattr(args, "id", None),
                "task": getattr(args, "task", None),
                "status": getattr(args, "status", None),
            }
            execute_command(command_dict, tasks, DATA_FILE)

    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}")
