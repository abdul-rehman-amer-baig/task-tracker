from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from ai.providers.base_provider import AIProvider
from ai.providers.provider_factory import AIProviderFactory
from ai.prompt_loader import load_prompt


class BaseAgent(ABC):
    def __init__(self, provider: Optional[AIProvider] = None):
        self.provider = provider or AIProviderFactory.get_default_provider()

    @property
    @abstractmethod
    def prompt_name(self) -> str:
        pass

    @abstractmethod
    def process_response(self, response: str, **kwargs) -> any:
        pass

    def _get_system_prompt(self) -> str:
        return load_prompt(self.prompt_name)

    def _call_provider(
        self,
        user_prompt: str,
        conversation_history: Optional[List[Dict]] = None,
    ) -> str:
        system_prompt = self._get_system_prompt()

        response = self.provider.ask(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            conversation_history=conversation_history,
        )

        if not response:
            raise RuntimeError(
                f"{self.__class__.__name__} returned an empty response. "
                f"This may be due to: API rate limiting, model not responding, or network issues. "
                f"Try again or check your API configuration."
            )

        response = response.strip()

        if not response:
            raise RuntimeError(
                f"{self.__class__.__name__} returned a whitespace-only response. "
                f"Provider may have returned empty content."
            )

        return response
