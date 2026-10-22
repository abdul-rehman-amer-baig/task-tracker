"""Agent Factory - Creates and manages agent instances"""

from __future__ import annotations

from ai.agents.command_agent import CommandAgent
from ai.agents.conversation_agent import ConversationAgent
from ai.agents.master_agent import MasterAgent
from ai.agents.python_agent import PythonAgent
from ai.providers.base_provider import AIProvider


class AgentFactory:
    @staticmethod
    def create_master_agent(provider: AIProvider | None = None) -> MasterAgent:
        return MasterAgent(provider=provider)

    @staticmethod
    def create_command_agent(provider: AIProvider | None = None) -> CommandAgent:
        return CommandAgent(provider=provider)

    @staticmethod
    def create_conversation_agent(
        provider: AIProvider | None = None,
    ) -> ConversationAgent:
        return ConversationAgent(provider=provider)

    @staticmethod
    def create_python_agent(provider: AIProvider | None = None) -> PythonAgent:
        return PythonAgent(provider=provider)
