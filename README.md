# Task Tracker CLI

A simple **Python CLI Task Tracker** that allows you to add, update, delete, and list tasks with different statuses. This project follows **SOLID principles** for clean and maintainable code, and comes with **unit tests** using `pytest`.

This scope of this project will grow more as I am planning to integrate AI for agentic actions. Wish me luck up until I commit those changes.
The scope of this project will expand as I'm planning to integrate AI for agentic actions. Up until I commit the changes for the new feature request, wish me luck
---

## Features

- Add a new task
- Update an existing task
- Mark tasks as **in-progress** or **done**
- Delete tasks
- List tasks, optionally filtered by status
- Persist tasks in a JSON file
- Pretty table output using `tabulate`

---

## Installation

**1.** Clone the repository:

```bash
git clone https://github.com/abdul-rehman-amer-baig/task-tracker.git
cd task-tracker
```

**2.** Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

**3.** Install dependencies:

```bash
pip install -r requirements.txt
```
---

## Usage
Run the CLI:

```bash
python cli.py <command> [arguments]
```

**Commands:**
| Command            | Arguments     | Description                        |
| ------------------ | ------------- | ---------------------------------- |
| `add`              | `<task>`      | Add a new task                     |
| `update`           | `<id> <task>` | Update a task                      |
| `delete`           | `<id>`        | Delete a task                      |
| `mark-in-progress` | `<id>`        | Mark a task as in-progress         |
| `mark-done`        | `<id>`        | Mark a task as done                |
| `list`             | `[status]`    | List all tasks or filter by status |

**Example:**

```bash
python cli.py add "Learn pytest"
python cli.py list
python cli.py mark-done 1
python cli.py delete 1
```
---

## Project Structure

```
task-tracker/
├─ cli.py                # Command-line interface
├─ model.py              # Task model and Status enums
├─ task_logic.py         # Core task functions (SOLID-compliant)
├─ presentation.py       # Task formatting for display
├─ storage.py            # JSON persistence
├─ tests/                # Unit tests
│  ├─ __init__.py
│  └─ test_task_logic.py
└─ tasks.json            # Storage file for tasks (will be produced if you run it locally)
```
---
## Testing

Run unit tests using `pytest`:
```bash
pytest -v
```

- Tests cover:
    - Adding, updating, deleting tasks
    - Marking tasks as in-progress or done
    - Error handling (invalid task IDs)
    - Filtering tasks by status

---
## Notes:
- This project separates core logic, application services, and presentation, making it easier to maintain and extend.
- The JSON storage file can be replaced with a database in the future without changing core logic.
- Follow SOLID principles: single responsibility, open/closed, and dependency injection using `save_fn` callbacks.

---
If you find any bugs, I’ll be monitoring [GitHub Issues](https://github.com/abdul-rehman-amer-baig/task-tracker/issues)
. Feel free to report them.

To learn more about the project details, check out the [roadmap](https://roadmap.sh/projects/task-tracker).

Want to know more about my professional experience and background? Click here to view the details: https://abdul-rehman-amer-baig.github.io/resume.pdf

---