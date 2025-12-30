import re
import json
from typing import Optional, List, Dict, Union
from ai.providers.provider_factory import AIProviderFactory
from ai.providers.base_provider import AIProvider
from ai.prompt_loader import load_prompt


def generate_code(
    question: str,
    tasks_data: Union[str, List[Dict]],
    provider: Optional[AIProvider] = None,
) -> str:
    if isinstance(tasks_data, (list, dict)):
        tasks_data = json.dumps(tasks_data, indent=2)

    system_prompt = load_prompt("python_agent.prompt")
    user_prompt = f"Question: {question}\n\nTasks data:\n{tasks_data}\n\nReturn ONLY the Python code:"

    if provider is None:
        provider = AIProviderFactory.get_default_provider()

    response = provider.ask(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        conversation_history=None,
    )

    response = response.strip() if response else ""

    if not response:
        raise RuntimeError("Python agent returned an empty response")

    code = _extract_code(response)

    return code


def _extract_code(text: str) -> str:
    python_match = re.search(r"```(?:python)?\s*(.+?)\s*```", text, re.DOTALL)
    if python_match:
        return python_match.group(1).strip()

    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("Question:"):
            return line.strip()

    return text.strip()
