import os
from typing import Optional
from .providers.base_provider import AIProvider
from .providers.openrouter_provider import OpenRouterProvider


class AIProviderFactory:
    @staticmethod
    def create_provider(provider_name: Optional[str] = None) -> AIProvider:
        if provider_name is None:
            provider_name = os.getenv("AI_PROVIDER", "openrouter").lower()

        provider_name = provider_name.lower()

        if provider_name == "openrouter":
            return OpenRouterProvider()
        else:
            raise ValueError(
                f"Unknown AI provider: {provider_name}. Available: openrouter"
            )

    @staticmethod
    def get_default_provider() -> AIProvider:
        return AIProviderFactory.create_provider()
