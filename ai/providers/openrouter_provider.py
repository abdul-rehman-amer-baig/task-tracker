import os
import requests
from typing import Optional, List, Dict
from dotenv import load_dotenv
from ai.providers.base_provider import AIProvider

load_dotenv()


class OpenRouterProvider(AIProvider):
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.url = os.getenv(
            "OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions"
        )
        self.model = os.getenv("AI_MODEL") or os.getenv("OPENROUTER_MODEL")

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not set. Add it to your .env file.")
        if not self.model:
            raise ValueError(
                "AI_MODEL or OPENROUTER_MODEL not set. Add it to your .env file."
            )

    def ask(
        self,
        system_prompt: Optional[str] = None,
        user_prompt: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None,
    ) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}"}

        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        if conversation_history:
            messages.extend(conversation_history)

        if user_prompt:
            messages.append({"role": "user", "content": user_prompt})
        else:
            raise ValueError("Must provide user_prompt")

        payload = {"model": self.model, "messages": messages, "temperature": 0}

        response = requests.post(self.url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        response_data = response.json()

        if "choices" not in response_data or not response_data["choices"]:
            raise RuntimeError(
                f"OpenRouter API returned no choices. Response: {response_data}"
            )

        content = response_data["choices"][0]["message"].get("content", "")

        if not content or not content.strip():
            raise RuntimeError(
                f"OpenRouter API returned empty content. "
                f"Model: {self.model}, "
                f"Response structure: {list(response_data.keys())}"
            )

        return content.strip()
