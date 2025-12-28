import pytest
from unittest.mock import MagicMock
from ai.parser import parse_human_input
from ai.providers.base_provider import AIProvider
from ai.schema import AddCommand, ListCommand, ConversationResponse

@pytest.fixture
def mock_provider():
    provider = MagicMock(spec=AIProvider)
    return provider

def test_parse_add_command(mock_provider):
    mock_provider.ask.return_value = """
    ```json
    {
      "type": "command",
      "command": "add",
      "task": "Write tests"
    }
    ```"""
    
    response = parse_human_input("Add task Write tests", provider=mock_provider)
    
    assert isinstance(response, AddCommand)
    assert response.task == "Write tests"

def test_parse_list_command(mock_provider):
    mock_provider.ask.return_value = """
    ```json
    {
      "type": "command",
      "command": "list",
      "status": "TODO"
    }
    ```"""
    
    response = parse_human_input("Show me TODO tasks", provider=mock_provider)
    
    assert isinstance(response, ListCommand)
    assert response.status == "TODO"

def test_parse_conversation_response(mock_provider):
    mock_provider.ask.return_value = """
    ```json
    {
      "type": "conversation",
      "message": "Hello, how can I help you?"
    }
    ```"""
    
    response = parse_human_input("Hi AI", provider=mock_provider)
    
    assert isinstance(response, ConversationResponse)
    assert response.message == "Hello, how can I help you?"
