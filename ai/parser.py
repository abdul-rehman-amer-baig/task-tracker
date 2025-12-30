from typing import Optional, List, Dict
from ai.providers.provider_factory import AIProviderFactory
from ai.providers.base_provider import AIProvider
from ai.schema.command_schemas import AIResponse
from ai.agents.agent_factory import AgentFactory
from ai.agents.router import route_to_agent


def parse_human_input(
    human_text: str,
    tasks: list = None,
    provider: Optional[AIProvider] = None,
    conversation_history: Optional[List[Dict]] = None,
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
