from model import Task
from typing import List
from tabulate import tabulate


def format_tasks_table(tasks: List[Task]) -> str:
    if not tasks:
        return "No tasks found."

    table_data = [[t.id, t.task, t.status, t.created_at, t.updated_at] for t in tasks]

    headers = ["ID", "Task", "Status", "Created At", "Updated At"]
    return tabulate(table_data, headers=headers, tablefmt="grid")
