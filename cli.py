import argparse
from model import Status


def parse_args():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ai_parser = subparsers.add_parser(
        "ai", help="Use AI to perform a task (e.g., 'mark my first task as done')"
    )
    ai_parser.add_argument(
        "text", type=str, help="Human instruction for AI to interpret"
    )

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
        choices=[Status.TODO, Status.IN_PROGRESS, Status.DONE],
        help="Filter tasks by status (TODO, IN_PROGRESS, DONE)",
    )

    return parser.parse_args()
