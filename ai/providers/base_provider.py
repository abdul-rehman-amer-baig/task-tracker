from __future__ import annotations

from abc import ABC, abstractmethod


class AIProvider(ABC):
    @abstractmethod
    def ask(
        self,
        system_prompt: str | None = None,
        user_prompt: str | None = None,
        conversation_history: list[dict] | None = None,
    ) -> str:
        pass
