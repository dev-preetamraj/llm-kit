from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from llm_kit_pro.core.inputs import LLMFile
from llm_kit_pro.providers.gemini.client import GeminiClient
from llm_kit_pro.providers.gemini.config import GeminiConfig


@pytest.mark.asyncio
async def test_generate_text_without_files():
    mock_response = MagicMock(text="Hello world")

    mock_models = MagicMock()
    mock_models.generate_content = MagicMock(return_value=mock_response)

    mock_client = MagicMock()
    mock_client.models = mock_models

    with patch.object(
        GeminiClient,
        "_create_client",
        return_value=mock_client,
    ):
        client = GeminiClient(GeminiConfig(api_key="fake-key"))

        result = await client.generate_text("Say hello")

        assert result == "Hello world"


@pytest.mark.asyncio
async def test_generate_text_with_file():
    fake_pdf = LLMFile(
        content=b"%PDF-1.4 fake pdf",
        mime_type="application/pdf",
        filename="bill.pdf",
    )

    mock_response = MagicMock(text="Bill summary")
    mock_uploaded_file = MagicMock()

    mock_models = MagicMock()
    mock_models.generate_content = MagicMock(return_value=mock_response)

    mock_files = MagicMock()
    mock_files.upload = MagicMock(return_value=mock_uploaded_file)

    mock_client = MagicMock()
    mock_client.models = mock_models
    mock_client.files = mock_files

    with patch.object(
        GeminiClient,
        "_create_client",
        return_value=mock_client,
    ):
        client = GeminiClient(GeminiConfig(api_key="fake-key"))

        result = await client.generate_text(
            "Summarize this bill",
            files=[fake_pdf],
        )

        assert result == "Bill summary"


@pytest.mark.asyncio
async def test_generate_json():
    class AmountSchema(BaseModel):
        amount: float

    expected_data = {"amount": 123.45}
    # For Gemini, the SDK might return the model instance if passed Type[BaseModel]
    mock_response = MagicMock(parsed=AmountSchema(**expected_data))

    mock_models = MagicMock()
    mock_models.generate_content = MagicMock(return_value=mock_response)

    mock_client = MagicMock()
    mock_client.models = mock_models

    with patch.object(
        GeminiClient,
        "_create_client",
        return_value=mock_client,
    ):
        client = GeminiClient(GeminiConfig(api_key="fake-key"))

        result = await client.generate_json(
            prompt="Extract amount",
            schema=AmountSchema,
        )

        assert result == expected_data
