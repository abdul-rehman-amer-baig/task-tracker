from model import Status, Task
from storage import save_json
from tabulate import tabulate


def add_task(tasks: list[Task], args, data_file):
    tasks.append(
        Task(
            id=len(tasks) + 1 if tasks else 1,
            task=args.task,
        )
    )

    save_json(tasks, data_file)

    print("Task added successfully")
    return tasks[-1]


def update_task_generic(tasks: list[Task], args, data_file, update_function):
    id_exists = False
    for i in range(len(tasks)):
        if tasks[i].id == args.id:
            id_exists = True
            update_function(tasks[i])
            tasks[i].mark_updated()
            break

    if not id_exists:
        raise ValueError(f"Task with ID {args.id} not found")

    save_json(tasks, data_file)
    return tasks[args.id - 1]


def update_task(tasks: list[Task], args, data_file):
    return update_task_generic(
        tasks, args, data_file, lambda task: setattr(task, "task", args.task)
    )


def mark_in_progress_task(tasks: list[Task], args, data_file):
    return update_task_generic(
        tasks, args, data_file, lambda task: setattr(task, "status", Status.IN_PROGRESS)
    )


def mark_done_task(tasks: list[Task], args, data_file):
    return update_task_generic(
        tasks, args, data_file, lambda task: setattr(task, "status", Status.DONE)
    )


def delete_task(tasks: list[Task], args, data_file):
    id_exists = False
    for i in range(len(tasks)):
        if tasks[i].id == args.id:
            id_exists = True
            tasks.pop(i)
            break

    if not id_exists:
        raise ValueError(f"Task with ID {args.id} not found")

    save_json(tasks, data_file)
    return f"Task deleted successfully (ID: {args.id})"


def filter_task_by_status(tasks: list[Task], status: Status):
    return [task for task in tasks if task.status == status]


def display_tasks(tasks: list[Task]):
    if not tasks:
        print("No tasks found.")
        return

    # Prepare data for tabulate
    table_data = []
    for task in tasks:
        table_data.append(
            [task.id, task.task, task.status, task.created_at, task.updated_at]
        )

    # Create table with headers
    headers = ["ID", "Task", "Status", "Created At", "Updated At"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def list_tasks(tasks: list[Task], args):
    if args.status:
        filtered_tasks = filter_task_by_status(tasks, args.status)
    else:
        filtered_tasks = tasks
    display_tasks(filtered_tasks)
