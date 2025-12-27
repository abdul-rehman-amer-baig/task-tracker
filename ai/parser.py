from typing import Optional, List, Dict
from .provider_factory import AIProviderFactory
from .providers.base_provider import AIProvider
import json
import re


def parse_human_input(
    human_text: str,
    tasks: list = None,
    provider: Optional[AIProvider] = None,
    conversation_history: Optional[List[Dict]] = None,
) -> dict:
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
            }
            for task in tasks
        ]
        tasks_data = json.dumps(tasks_list, indent=2)

    system_prompt = """You are a TODO task manager. Convert user requests to JSON commands.

        Response format (JSON only, no extra text):
        - Commands: {{"type": "command", "command": "<cmd>", "id": <id>, "task": "<text>", "status": "<status>", "message": "<optional>"}}
        - Questions: {{"type": "conversation", "message": "<text>"}}

        Commands: "add", "update", "delete", "mark-done", "mark-in-progress", "list"
        Statuses: "TODO", "IN_PROGRESS", "DONE", null

        CRITICAL - Always include "status" field:
        - For "list" command: ALWAYS include "status" field
          * "status": null → show ALL tasks (use when user says "list tasks", "show tasks", "display tasks" without specifying status)
          * "status": "TODO" → show only TODO tasks
          * "status": "IN_PROGRESS" → show only IN_PROGRESS tasks
          * "status": "DONE" → show only DONE tasks
        - For other commands: include "status" only if relevant (usually not needed)

        IMPORTANT:
        - Only include "message" field if user EXPLICITLY asks a question in the same request
          Example: "what's my name and show tasks" → {{"type": "command", "command": "list", "status": null, "message": "Your name is ARA. Here are your tasks:"}}
          Example: "display tasks" → {{"type": "command", "command": "list", "status": null}} (NO message field)
        - Do NOT add information to messages just because it's in conversation history - only if user asks for it NOW
        - "update" = change task TEXT only. "update status" → use "mark-in-progress" or "mark-done"
        - "find/show/list" → use "list" command with "status": null (never return task data in conversation)
        - "most recent/last" → task with LATEST created_at timestamp
        - Missing info → ask follow-up question
        - Return ONLY valid JSON, no text before or after"""

    context_prompt = (
        f"""Current tasks:
        {tasks_data}

        Use this to: find IDs by description, match task names, or identify most recent task.
        Most recent = task with the LATEST created_at timestamp (chronologically newest/highest value)."""
        if tasks_data
        else ""
    )

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


def _validate_and_normalize_response(parsed: dict) -> dict:
    if not isinstance(parsed, dict):
        raise ValueError("Response must be a JSON object")

    response_type = parsed.get("type")

    if response_type == "command":
        if "command" not in parsed:
            raise ValueError("Command type must include 'command' field")
        return parsed
    elif response_type == "conversation":
        if "message" not in parsed:
            raise ValueError("Conversation type must include 'message' field")
        return parsed
    else:
        if "command" in parsed:
            parsed["type"] = "command"
            return parsed
        else:
            raise ValueError(
                "Response must have either 'type': 'command' or 'type': 'conversation'"
            )
