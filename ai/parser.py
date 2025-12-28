from typing import Optional, List, Dict
from dataclasses import fields
from .provider_factory import AIProviderFactory
from .providers.base_provider import AIProvider
from .prompt_loader import load_prompt
from .schema import (
    AddCommand,
    UpdateCommand,
    DeleteCommand,
    MarkDoneCommand,
    MarkInProgressCommand,
    ListCommand,
    ConversationResponse,
    AIResponse,
)
import json
import re


def parse_human_input(
    human_text: str,
    tasks: list = None,
    provider: Optional[AIProvider] = None,
    conversation_history: Optional[List[Dict]] = None,
) -> AIResponse:
    tasks_data = ""
    if tasks:
        tasks_list = [
            {
                "id": task.id,
                "task": task.task,
                "status": task.status,
                "created_at": task.created_at.isoformat()
                if hasattr(task.created_at, "isoformat")
                else str(task.created_at),
                "updated_at": task.updated_at.isoformat()
                if hasattr(task.updated_at, "isoformat")
                else str(task.updated_at),
            }
            for task in tasks
        ]
        tasks_data = json.dumps(tasks_list, indent=2)

    system_prompt = load_prompt("command_parser.prompt")

    context_prompt = ""
    if tasks_data:
        context_template = load_prompt("task_context.prompt")
        context_prompt = context_template.format(tasks_data=tasks_data)

    user_prompt = f'User: "{human_text}"'

    full_system_prompt = system_prompt
    if context_prompt:
        full_system_prompt = f"{system_prompt}\n\n{context_prompt}"

    if provider is None:
        provider = AIProviderFactory.get_default_provider()

    response = provider.ask(
        system_prompt=full_system_prompt,
        user_prompt=user_prompt,
        conversation_history=conversation_history,
    )

    response = response.strip() if response else ""

    if not response:
        raise RuntimeError(
            "AI model returned an empty response. "
            "The free Mistral model may not be suitable for structured JSON output. "
            "Consider using a better model like 'openai/gpt-3.5-turbo' or 'anthropic/claude-3-haiku' in your .env file."
        )

    json_text = _extract_json(response)

    try:
        parsed = json.loads(json_text)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"AI model returned invalid JSON: {repr(response[:100])}. "
            f"Error: {e}. "
            "The free Mistral model may not be following instructions properly. "
            "Consider using a better model in your .env file (e.g., 'openai/gpt-3.5-turbo')."
        )

    return _validate_and_normalize_response(parsed)


def _validate_and_normalize_response(parsed: dict) -> AIResponse:
    response_type = parsed.get("type")

    if response_type == "conversation":
        return _create_dataclass(ConversationResponse, parsed)

    if response_type != "command":
        if "command" in parsed:
            parsed["type"] = "command"
        else:
            raise ValueError(
                "Response must have either 'type': 'command' or 'type': 'conversation'"
            )

    cmd = parsed.get("command")
    if not cmd:
        raise ValueError("Command type must include 'command' field")

    if cmd == "add":
        return _create_dataclass(AddCommand, parsed)
    elif cmd == "update":
        return _create_dataclass(UpdateCommand, parsed)
    elif cmd == "delete":
        return _create_dataclass(DeleteCommand, parsed)
    elif cmd == "mark-done":
        return _create_dataclass(MarkDoneCommand, parsed)
    elif cmd == "mark-in-progress":
        return _create_dataclass(MarkInProgressCommand, parsed)
    elif cmd == "list":
        return _create_dataclass(ListCommand, parsed)
    else:
        raise ValueError(f"Unknown command: {cmd}")


def _create_dataclass(dataclass_class, data: dict):
    field_names = {f.name for f in fields(dataclass_class)}
    filtered_data = {k: v for k, v in data.items() if k in field_names}
    return dataclass_class(**filtered_data)


def _extract_json(text: str) -> str:
    json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if json_match:
        return json_match.group(1).strip()

    json_start = text.find('{"type"')
    if json_start == -1:
        json_start = text.find('{"command"')

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
