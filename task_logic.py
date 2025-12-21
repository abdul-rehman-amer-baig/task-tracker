from model import Status, Task
from storage import save_json


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


def list_tasks(tasks: list[Task], args):
    filtered_tasks = []
    if args.status == Status.DONE:
        filtered_tasks = [task for task in tasks if task.status == Status.DONE]
    elif args.status == Status.TODO:
        filtered_tasks = [task for task in tasks if task.status == Status.TODO]
    elif args.status == Status.IN_PROGRESS:
        filtered_tasks = [task for task in tasks if task.status == Status.IN_PROGRESS]
    else:
        filtered_tasks = tasks

    for task in filtered_tasks:
        print(task)
