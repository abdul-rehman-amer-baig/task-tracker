"""Agent Factory - Creates and manages agent instances"""

from typing import Optional
from ai.providers.base_provider import AIProvider
from ai.agents.master_agent import MasterAgent
from ai.agents.command_agent import CommandAgent
from ai.agents.conversation_agent import ConversationAgent
from ai.agents.python_agent import PythonAgent


class AgentFactory:
    @staticmethod
    def create_master_agent(provider: Optional[AIProvider] = None) -> MasterAgent:
        return MasterAgent(provider=provider)

    @staticmethod
    def create_command_agent(provider: Optional[AIProvider] = None) -> CommandAgent:
        return CommandAgent(provider=provider)

    @staticmethod
    def create_conversation_agent(
        provider: Optional[AIProvider] = None,
    ) -> ConversationAgent:
        return ConversationAgent(provider=provider)

    @staticmethod
    def create_python_agent(provider: Optional[AIProvider] = None) -> PythonAgent:
        return PythonAgent(provider=provider)
