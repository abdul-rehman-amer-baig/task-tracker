import re
import json
from typing import List, Dict, Union
from ai.agents.base_agent import BaseAgent


class PythonAgent(BaseAgent):
    @property
    def prompt_name(self) -> str:
        return "python_agent.prompt"

    def generate_code(
        self,
        question: str,
        tasks_data: Union[str, List[Dict]],
    ) -> str:
        if isinstance(tasks_data, (list, dict)):
            tasks_data = json.dumps(tasks_data, indent=2)

        user_prompt = f"Question: {question}\n\nTasks data:\n{tasks_data}\n\nReturn ONLY the Python code:"
        response = self._call_provider(user_prompt, conversation_history=None)

        return self.process_response(response)

    def process_response(self, response: str, **kwargs) -> str:
        return self._extract_code(response)

    def _extract_code(self, text: str) -> str:
        python_match = re.search(r"```(?:python)?\s*(.+?)\s*```", text, re.DOTALL)
        if python_match:
            code = python_match.group(1).strip()
            if code:
                return code

        lines = text.split("\n")
        code_lines = []
        skip_prefixes = ["Question:", "# Question", "Tasks data:", "Return"]

        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#") and not code_lines:
                continue
            if any(line.startswith(prefix) for prefix in skip_prefixes):
                continue
            if line and (not line.startswith("#") or code_lines):
                code_lines.append(line)

        if code_lines:
            return "\n".join(code_lines).strip()

        return text.strip()
