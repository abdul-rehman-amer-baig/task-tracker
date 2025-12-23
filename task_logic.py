from model import Status, Task
from storage import save_json
from tabulate import tabulate
from typing import List, Callable


# * CORE LOGIC FUNCTIONS
def create_task(tasks: List[Task], task_text: str) -> Task:
    new_task = Task(
        id=len(tasks) + 1 if tasks else 1,
        task=task_text,
    )
    tasks.append(new_task)
    return new_task


def update_task_generic(
    tasks: List[Task], task_id: int, update_fn: Callable[[Task], None]
) -> Task:
    for task in tasks:
        if task.id == task_id:
            update_fn(task)
            task.mark_updated()
            return task

    raise ValueError(f"Task with ID {task_id} not found")


def delete_task_by_id(tasks: List[Task], task_id: int) -> Task:
    for task in tasks:
        if task.id == task_id:
            tasks.pop(task_id - 1)
            return task

    raise ValueError(f"Task with ID {task_id} not found")


def filter_task_by_status(tasks: list[Task], status: Status):
    return [task for task in tasks if task.status == status]


# * APLICATION SERVICES (ORCHESTRATION)
def add_task(
    tasks: list[Task], task_text: str, save_fn: Callable[[List[Task]], None]
) -> Task:
    task = create_task(tasks, task_text)
    save_fn(tasks)
    return task


def update_task(
    tasks: list[Task],
    task_id: int,
    task_text: str,
    save_fn: Callable[[List[Task]], None],
) -> Task:
    task = update_task_generic(
        tasks,
        task_id,
        lambda task: setattr(task, "task", task_text),
    )
    save_fn(tasks)
    return task


def mark_in_progress_task(
    tasks: list[Task], task_id: int, save_fn: Callable[[List[Task]], None]
) -> Task:
    task = update_task_generic(
        tasks,
        task_id,
        lambda task: setattr(task, "status", Status.IN_PROGRESS),
    )
    save_fn(tasks)
    return task


def mark_done_task(
    tasks: list[Task], task_id: int, save_fn: Callable[[List[Task]], None]
) -> Task:
    task = update_task_generic(
        tasks,
        task_id,
        lambda task: setattr(task, "status", Status.DONE),
    )
    save_fn(tasks)
    return task


def delete_task(
    tasks: list[Task], task_id: int, save_fn: Callable[[List[Task]], None]
) -> Task:
    task = delete_task_by_id(tasks, task_id)
    save_fn(tasks)
    return task


def list_tasks(
    tasks: List[Task],
    status: Status = Status.TODO,
) -> List[Task]:
    filtered_tasks = filter_task_by_status(tasks, status)

    return filtered_tasks
