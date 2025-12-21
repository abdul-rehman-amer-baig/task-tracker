# Task Tracker CLI

A command-line interface (CLI) application to track and manage your tasks. This project helps you practice programming skills including working with the filesystem, handling user inputs, and building a simple CLI application.

**Project Reference:** [roadmap.sh - Task Tracker](https://roadmap.sh/projects/task-tracker)

## Features

The application allows you to:

- ✅ Add, Update, and Delete tasks
- ✅ Mark a task as in progress or done
- ✅ List all tasks
- ✅ List all tasks that are done
- ✅ List all tasks that are not done (todo)
- ✅ List all tasks that are in progress

## Task Properties

Each task has the following properties:

- `id`: A unique identifier for the task
- `task`: A short description of the task
- `status`: The status of the task (`TODO`, `IN_PROGRESS`, `DONE`)
- `created_at`: The date and time when the task was created
- `updated_at`: The date and time when the task was last updated

## Installation

1. Clone or download this repository
2. Ensure you have Python 3.x installed
3. No external dependencies required - uses only Python standard library

## Usage

Run the application using Python:

```bash
python main.py <command> [arguments]
```

### Commands

#### Add a new task

```bash
python main.py add "Buy groceries"
# Output: Task added successfully (ID: 1)
```

#### Update a task

```bash
python main.py update 1 "Buy groceries and cook dinner"
```

#### Delete a task

```bash
python main.py delete 1
```

#### Mark a task as in progress

```bash
python main.py mark-in-progress 1
```

#### Mark a task as done

```bash
python main.py mark-done 1
```

#### List all tasks

```bash
python main.py list
```

#### List tasks by status

```bash
python main.py list TODO
python main.py list IN_PROGRESS
python main.py list DONE
```

## Data Storage

Tasks are stored in a JSON file (`tasks.json`) in the current directory. The file is automatically created if it does not exist.

## Project Structure

```
task-tracker/
├── main.py          # Main entry point
├── cli.py           # Command-line argument parsing
├── model.py         # Task data model and Status enum
├── storage.py       # JSON file operations
├── task_logic.py    # Business logic for task operations
├── tasks.json       # Task data storage (auto-generated)
└── README.md        # This file
```

## Requirements

- Python 3.x
- No external libraries or frameworks required
- Uses native Python file system modules

## Error Handling

The application handles errors and edge cases gracefully, including:
- Invalid task IDs
- Empty task descriptions
- Missing or corrupted JSON files
- Invalid status values

## License

This project is part of the [roadmap.sh](https://roadmap.sh/projects/task-tracker) project collection.
