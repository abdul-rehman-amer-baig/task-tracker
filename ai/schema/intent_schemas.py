from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass
class IntentResponse:
    type: Literal["command", "computation", "conversation"]
    question: str | None = None
    command: str | None = None

    def __post_init__(self):
        if self.type == "computation":
            if not self.question:
                raise ValueError("computation type must include 'question' field")
            if not isinstance(self.question, str) or not self.question.strip():
                raise ValueError("question must be a non-empty string")

        if self.type == "command":
            if not self.command:
                raise ValueError("command type must include 'command' field")
            if not isinstance(self.command, str) or not self.command.strip():
                raise ValueError("command must be a non-empty string")
