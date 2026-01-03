import asyncio
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List

from pydantic import BaseModel

from llm_kit_pro.core.inputs import LLMFile
from llm_kit_pro.providers.openai.client import OpenAIClient
from llm_kit_pro.providers.openai.config import OpenAIConfig
from llm_kit_pro.settings import settings


class GreetingSchema(BaseModel):
    """Schema for greeting generation."""

    greeting: str
    language: str


class InfoExtractionSchema(BaseModel):
    """Schema for extracting information from text."""

    project_name: str
    description: str
    key_features: List[str]


class TestStrategy(ABC):
    """Base strategy interface for test cases."""

    @abstractmethod
    def get_name(self) -> str:
        """Return the name of this test strategy."""
        pass

    @abstractmethod
    async def execute(self, client: OpenAIClient) -> Any:
        """Execute the test strategy."""
        pass


class GenerateTextWithoutFileStrategy(TestStrategy):
    """Strategy for testing generate_text without file input."""

    def get_name(self) -> str:
        return "generate_text without file"

    async def execute(self, client: OpenAIClient) -> str:
        return await client.generate_text("Say hello in one sentence")


class GenerateTextWithFileStrategy(TestStrategy):
    """Strategy for testing generate_text with file input."""

    def get_name(self) -> str:
        return "generate_text with file"

    async def execute(self, client: OpenAIClient) -> str:
        readme_path = Path(__file__).parent.parent / "README.md"
        with open(readme_path, "rb") as f:
            readme_content = f.read()

        readme_file = LLMFile(
            content=readme_content, mime_type="text/plain", filename="README.md"
        )
        return await client.generate_text(
            "Summarize this README in one sentence", files=[readme_file]
        )


class GenerateJsonWithoutFileStrategy(TestStrategy):
    """Strategy for testing generate_json without file input."""

    def get_name(self) -> str:
        return "generate_json without file"

    async def execute(self, client: OpenAIClient) -> Dict[str, Any]:
        return await client.generate_json(
            "Generate a greeting in Spanish", schema=GreetingSchema
        )


class GenerateJsonWithFileStrategy(TestStrategy):
    """Strategy for testing generate_json with file input."""

    def get_name(self) -> str:
        return "generate_json with file"

    async def execute(self, client: OpenAIClient) -> Dict[str, Any]:
        readme_path = Path(__file__).parent.parent / "README.md"
        with open(readme_path, "rb") as f:
            readme_content = f.read()

        readme_file = LLMFile(
            content=readme_content, mime_type="text/plain", filename="README.md"
        )
        return await client.generate_json(
            "Extract project information from this README",
            schema=InfoExtractionSchema,
            files=[readme_file],
        )


class StrategyRunner:
    """Runs test strategies against a client."""

    def __init__(self, client: OpenAIClient):
        self.client = client

    async def run_strategy(self, strategy: TestStrategy) -> None:
        """Execute a single test strategy."""
        print("=" * 60)
        print(f"Test: {strategy.get_name()}")
        print("=" * 60)
        result = await strategy.execute(self.client)
        print(f"Result: {result}\n")

    async def run_all(self, strategies: List[TestStrategy]) -> None:
        """Execute all test strategies."""
        for strategy in strategies:
            await self.run_strategy(strategy)
        print("=" * 60)
        print("All tests completed!")
        print("=" * 60)


async def main():
    client = OpenAIClient(OpenAIConfig(api_key=settings.OEPNAI_API_KEY))

    strategies = [
        GenerateTextWithoutFileStrategy(),
        GenerateTextWithFileStrategy(),
        GenerateJsonWithoutFileStrategy(),
        GenerateJsonWithFileStrategy(),
    ]

    runner = StrategyRunner(client)
    await runner.run_all(strategies)


if __name__ == "__main__":
    asyncio.run(main())
