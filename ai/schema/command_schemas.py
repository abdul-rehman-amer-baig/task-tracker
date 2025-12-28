from dataclasses import dataclass, asdict
from typing import Optional, Literal, Union


@dataclass
class AddCommand:
    type: Literal["command"]
    command: Literal["add"]
    task: str
    message: Optional[str] = None

    def __post_init__(self):
        if self.type != "command":
            raise ValueError("type must be 'command'")
        if self.command != "add":
            raise ValueError("command must be 'add'")
        if not self.task or not isinstance(self.task, str):
            raise ValueError("task must be a non-empty string")

    def model_dump(self):
        return asdict(self)


@dataclass
class UpdateCommand:
    type: Literal["command"]
    command: Literal["update"]
    id: int
    task: str
    message: Optional[str] = None

    def __post_init__(self):
        if self.type != "command":
            raise ValueError("type must be 'command'")
        if self.command != "update":
            raise ValueError("command must be 'update'")
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("id must be a positive integer")
        if not self.task or not isinstance(self.task, str):
            raise ValueError("task must be a non-empty string")

    def model_dump(self):
        return asdict(self)


@dataclass
class DeleteCommand:
    type: Literal["command"]
    command: Literal["delete"]
    id: int
    message: Optional[str] = None

    def __post_init__(self):
        if self.type != "command":
            raise ValueError("type must be 'command'")
        if self.command != "delete":
            raise ValueError("command must be 'delete'")
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("id must be a positive integer")

    def model_dump(self):
        return asdict(self)


@dataclass
class MarkDoneCommand:
    type: Literal["command"]
    command: Literal["mark-done"]
    id: int
    message: Optional[str] = None

    def __post_init__(self):
        if self.type != "command":
            raise ValueError("type must be 'command'")
        if self.command != "mark-done":
            raise ValueError("command must be 'mark-done'")
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("id must be a positive integer")

    def model_dump(self):
        return asdict(self)


@dataclass
class MarkInProgressCommand:
    type: Literal["command"]
    command: Literal["mark-in-progress"]
    id: int
    message: Optional[str] = None

    def __post_init__(self):
        if self.type != "command":
            raise ValueError("type must be 'command'")
        if self.command != "mark-in-progress":
            raise ValueError("command must be 'mark-in-progress'")
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("id must be a positive integer")

    def model_dump(self):
        return asdict(self)


@dataclass
class ListCommand:
    type: Literal["command"]
    command: Literal["list"]
    status: Optional[Literal["TODO", "IN_PROGRESS", "DONE"]] = None
    message: Optional[str] = None

    def __post_init__(self):
        if self.type != "command":
            raise ValueError("type must be 'command'")
        if self.command != "list":
            raise ValueError("command must be 'list'")
        if self.status and self.status not in ("TODO", "IN_PROGRESS", "DONE"):
            raise ValueError("status must be one of: TODO, IN_PROGRESS, DONE")

    def model_dump(self):
        return asdict(self)


@dataclass
class ConversationResponse:
    type: Literal["conversation"]
    message: str

    def __post_init__(self):
        if self.type != "conversation":
            raise ValueError("type must be 'conversation'")
        if not self.message or not isinstance(self.message, str):
            raise ValueError("message must be a non-empty string")

    def model_dump(self):
        return asdict(self)


# Union type for all possible AI responses
AIResponse = Union[
    AddCommand,
    UpdateCommand,
    DeleteCommand,
    MarkDoneCommand,
    MarkInProgressCommand,
    ListCommand,
    ConversationResponse,
]
