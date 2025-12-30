import json
import re
from ai.schema.intent_schemas import IntentResponse
from ai.agents.base_agent import BaseAgent


class MasterAgent(BaseAgent):
    @property
    def prompt_name(self) -> str:
        return "master_agent.prompt"

    def classify_intent(self, human_text: str) -> IntentResponse:
        user_prompt = f'User: "{human_text}"'
        response = self._call_provider(user_prompt, conversation_history=None)

        json_text = self._extract_json(response)

        try:
            parsed = json.loads(json_text)
        except json.JSONDecodeError as e:
            raise RuntimeError(
                f"Master agent returned invalid JSON: {repr(response[:100])}. Error: {e}"
            )

        return self.process_response(response, human_text=human_text, parsed=parsed)

    def process_response(self, response: str, **kwargs) -> IntentResponse:
        parsed = kwargs.get("parsed")
        human_text = kwargs.get("human_text", "")

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

    def _extract_json(self, text: str) -> str:
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
