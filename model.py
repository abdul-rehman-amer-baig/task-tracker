from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Optional
from tabulate import tabulate


class Status:
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class CommandType:
    ADD = "add"
    UPDATE = "update"
    DELETE = "delete"
    MARK_DONE = "mark-done"
    MARK_IN_PROGRESS = "mark-in-progress"
    LIST = "list"


@dataclass
class Task:
    id: int
    task: str
    status: Status = Status.TODO
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def mark_updated(self):
        self.updated_at = datetime.now()

    def model_dump(self):
        task_dict = asdict(self)
        task_dict["created_at"] = self.created_at.isoformat()
        task_dict["updated_at"] = (
            self.updated_at.isoformat() if self.updated_at else None
        )
        return task_dict

    def __str__(self):
        return tabulate([self.model_dump()], headers="keys", tablefmt="grid")

    def __post_init__(self):
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)
        if isinstance(self.updated_at, str):
            self.updated_at = datetime.fromisoformat(self.updated_at)

        if not self.task.strip():
            raise ValueError("Task cannot be empty")
        if not self.id > 0:
            raise ValueError("ID must be greater than 0")
        if not isinstance(self.id, int):
            raise ValueError("ID must be an integer")
        if not isinstance(self.task, str):
            raise ValueError("Task must be a string")
