from __future__ import annotations

from ai.agents.agent_factory import AgentFactory
from ai.agents.router import route_to_agent
from ai.providers.base_provider import AIProvider
from ai.providers.provider_factory import AIProviderFactory
from ai.schema.command_schemas import AIResponse


def parse_human_input(
    human_text: str,
    tasks: list | None = None,
    provider: AIProvider | None = None,
    conversation_history: list[dict] | None = None,
) -> AIResponse:
    if provider is None:
        provider = AIProviderFactory.get_default_provider()

    master_agent = AgentFactory.create_master_agent(provider)
    intent = master_agent.classify_intent(human_text)
    print("Master Agent Intent: ", intent)

    return route_to_agent(
        intent,
        human_text,
        tasks,
        provider,
        conversation_history,
    )
