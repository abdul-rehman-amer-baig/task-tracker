Who Am I? Click to View My Resume → https://abdul-rehman-amer-baig.github.io/resume.pdf

# Description

This is a python CLI based task-tracker that allows you to perform CRUD operations on tasks. The codebase is aligned with SOLID, DRY principles and it also comes with unit testing via `pytest`. Not only that, I have amplified the scope of it by integrating an AI to perform CRUD on the behalf of user’s plain English.

---

### Features →

- Add a new task
- Update an existing task
- Mark tasks as **`in-progress`** or **`done`**
- Delete tasks
- List tasks, optionally filtered by status
- Persist tasks in a JSON file
- Use the above features not only by manual intervention but through AI as well

---

### Installation →

**1.** Clone the repository:

```bash
git clone <https://github.com/abdul-rehman-amer-baig/task-tracker.git>
cd task-tracker

```

**2.** Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\\Scripts\\activate      # Windows

```

**3.** Install dependencies:

```bash
pip install -r requirements.txt

```

---

### Usage without any help of AI →

Run the CLI:

```bash
python cli.py <command> [arguments]

```

**Commands:**

| Command | Arguments | Description |
| --- | --- | --- |
| `add` | `<task>` | Add a new task |
| `update` | `<id> <task>` | Update a task |
| `delete` | `<id>` | Delete a task |
| `mark-in-progress` | `<id>` | Mark a task as in-progress |
| `mark-done` | `<id>` | Mark a task as done |
| `list` | `[status]` | List all tasks or filter by status |

**Example:**

```bash
python cli.py add "Learn pytest"
python cli.py list
python cli.py mark-done 1
python cli.py delete 1

```

---

### How did I integrate AI →

I integrated AI in agentic approach where I have defined 4 kind of agents:

1. Master Agent (Acts as the orchestrator. It parses user intent from natural language and routes the request to the appropriate agent)
    1. Conversation Agent →
        - Handles basic, generic Q&A to keep the conversation natural and continuous.
    2. Command Agent 
        - The Master Agent transforms the user’s plain-English intent into a structured payload and invokes predefined application functions.
            - This agent does **not** have direct access to `tasks.json` (our database).
            - It can only operate through explicitly defined functions (e.g., `app.add_task`).
            - This constraint significantly reduces the risk of unintended actions, such as accidentally deleting tasks.
    3. Python Agent  (This particular agent is used to generate the python code to perform read-only operations as we cannot create all the possible combinations of the functions such as to fetch the most recent task, or count of `DONE` tasks and so forth. This agent has a responsibility to generate the python code and returns it then we execute the statement by validating the code through `AST (Abstract Syntax Tree)` to check if the code is free from malicious attempt such as `eval`, `os` etc.
    
    By splitting the roles to each of the agents the study says that it reduces the hallucination by 70%. Mind blown right?
    

---

## Project Structure

```
task-tracker/
├── ai/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── agent_factory.py
│   │   ├── base_agent.py
│   │   ├── command_agent.py
│   │   ├── conversation_agent.py
│   │   ├── master_agent.py
│   │   ├── python_agent.py
│   │   └── router.py
│   ├── parser.py
│   ├── prompt_loader.py
│   ├── prompts/
│   │   ├── command_parser.prompt
│   │   ├── conversation_agent.prompt
│   │   ├── master_agent.prompt
│   │   └── python_agent.prompt
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── base_provider.py
│   │   ├── openrouter_provider.py
│   │   └── provider_factory.py
│   ├── schema/
│   │   ├── __init__.py
│   │   ├── command_schemas.py
│   │   └── intent_schemas.py
│   └── validator.py
├── storage/
│   ├── __init__.py
│   ├── conversation_storage.py
│   └── json_storage.py
├── tests/
│   ├── __init__.py
│   ├── test_parse_ai_task.py
│   └── test_task_logic.py
├── cli.py
├── main.py
├── model.py
├── presentation.py
├── task_logic.py
├── README.md
├── requirements.txt
├── conversation_history.json
├── tasks.json
├── __pycache__/          (generated)
└── venv/                  (virtual environment)
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
    - Tested AI by giving the code hardcoded intents that master agent returns.

---

## Notes:

- This project separates core logic, application services, and presentation, making it easier to maintain and extend.
- The JSON storage file can be replaced with a database in the future without changing core logic.
- Follow SOLID, DRY principles.
- In AI domain, the roles and responsibilities are divided among multiple agents to reduce hallucinations to some extent.

---

If you find any bugs, I’ll be monitoring [GitHub Issues](https://github.com/abdul-rehman-amer-baig/task-tracker/issues). Feel free to report them.

To learn more about the project details, check out the [roadmap](https://roadmap.sh/projects/task-tracker).

Want to know more about my professional experience and background? Click here to view the details: https://abdul-rehman-amer-baig.github.io/resume.pdf

---