from typing import Optional, List, Dict
from ai.providers.provider_factory import AIProviderFactory
from ai.providers.base_provider import AIProvider
from ai.prompt_loader import load_prompt
from ai.schema.command_schemas import ConversationResponse


def reply(
    human_text: str,
    provider: Optional[AIProvider] = None,
    conversation_history: Optional[List[Dict]] = None,
) -> ConversationResponse:
    system_prompt = load_prompt("conversation_agent.prompt")
    user_prompt = f'User: "{human_text}"'

    if provider is None:
        provider = AIProviderFactory.get_default_provider()

    response = provider.ask(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        conversation_history=conversation_history,
    )

    response = response.strip() if response else ""

    if not response:
        raise RuntimeError("Conversation agent returned an empty response")

    message = _clean_response(response)

    return ConversationResponse(type="conversation", message=message)


def _clean_response(text: str) -> str:
    if "```" in text:
        lines = text.split("\n")
        cleaned = []
        in_code = False
        for line in lines:
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if not in_code:
                cleaned.append(line)
        return "\n".join(cleaned).strip()
    return text.strip()
