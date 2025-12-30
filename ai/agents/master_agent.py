from typing import Optional
import json
import re
from ai.providers.provider_factory import AIProviderFactory
from ai.providers.base_provider import AIProvider
from ai.prompt_loader import load_prompt
from ai.schema.intent_schemas import IntentResponse


def classify_intent(
    human_text: str,
    provider: Optional[AIProvider] = None,
) -> IntentResponse:
    system_prompt = load_prompt("master_agent.prompt")
    user_prompt = f'User: "{human_text}"'

    if provider is None:
        provider = AIProviderFactory.get_default_provider()

    response = provider.ask(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        conversation_history=None,
    )

    response = response.strip() if response else ""

    if not response:
        raise RuntimeError("Master agent returned an empty response")

    json_text = _extract_json(response)

    try:
        parsed = json.loads(json_text)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Master agent returned invalid JSON: {repr(response[:100])}. Error: {e}"
        )

    intent_type = parsed.get("type")
    if intent_type not in ("command", "computation", "conversation"):
        raise ValueError(
            f"Invalid intent type: {intent_type}. Must be 'command', 'computation', or 'conversation'"
        )

    if intent_type == "computation":
        return IntentResponse(
            type="computation", question=parsed.get("question", human_text)
        )
    elif intent_type == "command":
        return IntentResponse(type="command", command=parsed.get("command"))
    else:
        return IntentResponse(type="conversation")


def _extract_json(text: str) -> str:
    json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if json_match:
        return json_match.group(1).strip()

    json_start = text.find('{"type"')
    if json_start == -1:
        return text.strip()

    brace_count = 0
    for i in range(json_start, len(text)):
        if text[i] == "{":
            brace_count += 1
        elif text[i] == "}":
            brace_count -= 1
            if brace_count == 0:
                return text[json_start : i + 1].strip()

    return text[json_start:].strip()
