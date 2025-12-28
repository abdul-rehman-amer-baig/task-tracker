import pytest
from model import Task, Status
from task_logic import (
    add_task,
    update_task,
    delete_task,
    mark_in_progress_task,
    mark_done_task,
    list_tasks,
)


# ------------------------
# Dummy save function
# ------------------------
def dummy_save(tasks):
    pass 


# ------------------------
# ADD TASK
# ------------------------
def test_add_task():
    tasks = []
    new_task = add_task(tasks, "Write unit tests", dummy_save)

    assert new_task.id == 1
    assert new_task.task == "Write unit tests"
    assert new_task.status == Status.TODO
    assert len(tasks) == 1


# ------------------------
# UPDATE TASK
# ------------------------
def test_update_task():
    tasks = [Task(id=1, task="Old task")]

    updated = update_task(tasks, 1, "New task text", dummy_save)
    assert updated.task == "New task text"


def test_update_task_invalid_id():
    tasks = [Task(id=1, task="Old task")]

    with pytest.raises(ValueError) as excinfo:
        update_task(tasks, 99, "New task text", dummy_save)
    assert "Task with ID 99 not found" in str(excinfo.value)


# ------------------------
# MARK TASK IN PROGRESS
# ------------------------
def test_mark_in_progress():
    tasks = [Task(id=1, task="Some task")]

    task = mark_in_progress_task(tasks, 1, dummy_save)
    assert task.status == Status.IN_PROGRESS


# ------------------------
# MARK TASK DONE
# ------------------------
def test_mark_done():
    tasks = [Task(id=1, task="Some task")]

    task = mark_done_task(tasks, 1, dummy_save)
    assert task.status == Status.DONE


# ------------------------
# DELETE TASK
# ------------------------
def test_delete_task():
    tasks = [Task(id=1, task="Delete me")]
    deleted_task = delete_task(tasks, 1, dummy_save)

    assert deleted_task.task == "Delete me"
    assert len(tasks) == 0


def test_delete_task_invalid_id():
    tasks = [Task(id=1, task="Task")]
    with pytest.raises(ValueError) as excinfo:
        delete_task(tasks, 99, dummy_save)
    assert "Task with ID 99 not found" in str(excinfo.value)


# ------------------------
# LIST TASKS BY STATUS
# ------------------------
def test_list_tasks_by_status():
    tasks = [
        Task(id=1, task="Task 1"),
        Task(id=2, task="Task 2", status=Status.IN_PROGRESS),
        Task(id=3, task="Task 3", status=Status.DONE),
    ]

    todo_tasks = list_tasks(tasks, status=Status.TODO)
    in_progress_tasks = list_tasks(tasks, status=Status.IN_PROGRESS)
    done_tasks = list_tasks(tasks, status=Status.DONE)

    assert len(todo_tasks) == 1
    assert todo_tasks[0].task == "Task 1"
    assert len(in_progress_tasks) == 1
    assert in_progress_tasks[0].task == "Task 2"
    assert len(done_tasks) == 1
    assert done_tasks[0].task == "Task 3"
