from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from llm_kit_pro.core.inputs import LLMFile
from llm_kit_pro.providers.openai.client import OpenAIClient
from llm_kit_pro.providers.openai.config import OpenAIConfig


@pytest.fixture
def mock_openai_client():
    with patch("openai.OpenAI") as mock:
        yield mock


@pytest.mark.asyncio
async def test_generate_text_without_files(mock_openai_client):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Hello world"

    mock_instance = mock_openai_client.return_value
    mock_instance.chat.completions.create.return_value = mock_response

    client = OpenAIClient(OpenAIConfig(api_key="fake-key", model="gpt-4o"))
    result = await client.generate_text("Say hello")

    assert result == "Hello world"
    mock_instance.chat.completions.create.assert_called_once()
    args, kwargs = mock_instance.chat.completions.create.call_args
    assert kwargs["messages"] == [{"role": "user", "content": "Say hello"}]


@pytest.mark.asyncio
async def test_generate_text_with_image_file(mock_openai_client):
    fake_image = LLMFile(
        content=b"fake-image-data",
        mime_type="image/png",
        filename="test.png",
    )

    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "I see an image"

    mock_instance = mock_openai_client.return_value
    mock_instance.chat.completions.create.return_value = mock_response

    client = OpenAIClient(OpenAIConfig(api_key="fake-key", model="gpt-4o"))
    result = await client.generate_text(
        "What is this?",
        files=[fake_image],
    )

    assert result == "I see an image"
    mock_instance.chat.completions.create.assert_called_once()
    args, kwargs = mock_instance.chat.completions.create.call_args

    messages = kwargs["messages"]
    assert len(messages[0]["content"]) == 2
    assert messages[0]["content"][0]["type"] == "text"
    assert messages[0]["content"][1]["type"] == "image_url"
    assert "data:image/png;base64," in messages[0]["content"][1]["image_url"]["url"]


@pytest.mark.asyncio
async def test_generate_json(mock_openai_client):
    class AmountSchema(BaseModel):
        amount: float

    expected_data = {"amount": 123.45}

    mock_response = MagicMock()
    mock_message = MagicMock()
    mock_message.refusal = None
    mock_message.parsed = AmountSchema(**expected_data)
    mock_response.choices = [MagicMock(message=mock_message)]

    mock_instance = mock_openai_client.return_value
    mock_instance.beta.chat.completions.parse.return_value = mock_response

    client = OpenAIClient(OpenAIConfig(api_key="fake-key", model="gpt-4o"))
    result = await client.generate_json(
        prompt="Extract amount",
        schema=AmountSchema,
    )

    assert result == expected_data
    mock_instance.beta.chat.completions.parse.assert_called_once()
    _, kwargs = mock_instance.beta.chat.completions.parse.call_args
    assert kwargs["response_format"] == AmountSchema
