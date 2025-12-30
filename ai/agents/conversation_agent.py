from typing import Optional, List, Dict
from ai.schema.command_schemas import ConversationResponse
from ai.agents.base_agent import BaseAgent


class ConversationAgent(BaseAgent):
    @property
    def prompt_name(self) -> str:
        return "conversation_agent.prompt"

    def reply(
        self,
        human_text: str,
        conversation_history: Optional[List[Dict]] = None,
    ) -> ConversationResponse:
        user_prompt = f'User: "{human_text}"'
        response = self._call_provider(
            user_prompt, conversation_history=conversation_history
        )

        return self.process_response(response)

    def process_response(self, response: str, **kwargs) -> ConversationResponse:
        message = self._clean_response(response)
        return ConversationResponse(type="conversation", message=message)

    def _clean_response(self, text: str) -> str:
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
