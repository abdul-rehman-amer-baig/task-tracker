from abc import ABC, abstractmethod
from typing import Optional, List, Dict


class AIProvider(ABC):
    @abstractmethod
    def ask(
        self,
        system_prompt: Optional[str] = None,
        user_prompt: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None,
    ) -> str:
        pass
