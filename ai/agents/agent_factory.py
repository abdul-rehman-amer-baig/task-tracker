from typing import Optional, List, Dict
from ai.providers.base_provider import AIProvider
from ai.schema.intent_schemas import IntentResponse
from ai.schema.command_schemas import AIResponse, ConversationResponse
from ai.validator import safe_evaluate, ReadOnlyValidationError
from ai.agents.conversation_agent import reply
from ai.agents.python_agent import generate_code
from ai.agents.command_agent import handle_command


def route_to_agent(
    intent: IntentResponse,
    human_text: str,
    tasks: list = None,
    provider: Optional[AIProvider] = None,
    conversation_history: Optional[List[Dict]] = None,
) -> AIResponse:
    if intent.type == "command":
        result = handle_command(
            human_text,
            provider,
        )
        print(result)
        return result
    elif intent.type == "computation":
        tasks_data = []
        if tasks:
            tasks_data = [
                {
                    "id": task.id,
                    "task": task.task,
                    "status": task.status
                    if isinstance(task.status, str)
                    else str(task.status),
                    "created_at": task.created_at.isoformat()
                    if hasattr(task.created_at, "isoformat")
                    else str(task.created_at),
                    "updated_at": task.updated_at.isoformat()
                    if hasattr(task.updated_at, "isoformat")
                    else str(task.updated_at),
                }
                for task in tasks
            ]

        code = generate_code(intent.question, tasks_data, provider)

        try:
            result = safe_evaluate(code, tasks_data)
            print("The python code is: ", code)
            message = f"The answer is: {result}"
        except ReadOnlyValidationError as e:
            message = f"Error: Code validation failed - {e}"
        except Exception as e:
            message = f"Error executing code: {e}"

        return ConversationResponse(type="conversation", message=message)

    else:  # conversation
        return reply(human_text, provider, conversation_history)
