import asyncio
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List

from pydantic import BaseModel

from llm_kit.core.inputs import LLMFile
from llm_kit.providers.gemini.client import GeminiClient
from llm_kit.providers.gemini.config import GeminiConfig
from llm_kit.settings import settings


class GreetingSchema(BaseModel):
    """Schema for greeting generation."""

    greeting: str
    language: str


class BillExtractionSchema(BaseModel):
    """Schema for extracting bill information from PDF."""

    consumer_name: str
    bill_amount: float
    due_date: str
    account_number: str


class TestStrategy(ABC):
    """Base strategy interface for test cases."""

    @abstractmethod
    def get_name(self) -> str:
        """Return the name of this test strategy."""
        pass

    @abstractmethod
    async def execute(self, client: GeminiClient) -> Any:
        """Execute the test strategy."""
        pass


class GenerateTextWithoutFileStrategy(TestStrategy):
    """Strategy for testing generate_text without file input."""

    def get_name(self) -> str:
        return "generate_text without file"

    async def execute(self, client: GeminiClient) -> str:
        return await client.generate_text("Say hello in one sentence")


class GenerateTextWithFileStrategy(TestStrategy):
    """Strategy for testing generate_text with file input."""

    def get_name(self) -> str:
        return "generate_text with file"

    async def execute(self, client: GeminiClient) -> str:
        bill_path = Path(__file__).parent.parent / "bill.pdf"
        with open(bill_path, "rb") as f:
            bill_content = f.read()

        bill_file = LLMFile(
            content=bill_content,
            mime_type="application/pdf",
            filename="bill.pdf"
        )
        return await client.generate_text(
            "Summarize this bill in one sentence",
            files=[bill_file]
        )


class GenerateJsonWithoutFileStrategy(TestStrategy):
    """Strategy for testing generate_json without file input."""

    def get_name(self) -> str:
        return "generate_json without file"

    async def execute(self, client: GeminiClient) -> Dict[str, Any]:
        schema = GreetingSchema.model_json_schema()
        return await client.generate_json(
            "Generate a greeting in Spanish",
            schema=schema
        )


class GenerateJsonWithFileStrategy(TestStrategy):
    """Strategy for testing generate_json with file input."""

    def get_name(self) -> str:
        return "generate_json with file"

    async def execute(self, client: GeminiClient) -> Dict[str, Any]:
        bill_path = Path(__file__).parent.parent / "bill.pdf"
        with open(bill_path, "rb") as f:
            bill_content = f.read()

        bill_file = LLMFile(
            content=bill_content,
            mime_type="application/pdf",
            filename="bill.pdf"
        )
        schema = BillExtractionSchema.model_json_schema()
        return await client.generate_json(
            "Extract the billing information from this document",
            schema=schema,
            files=[bill_file]
        )


class StrategyRunner:
    """Runs test strategies against a client."""

    def __init__(self, client: GeminiClient):
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
    client = GeminiClient(
        GeminiConfig(
            api_key=settings.GEMINI_API_KEY
        )
    )

    strategies = [
        # GenerateTextWithoutFileStrategy(),
        # GenerateTextWithFileStrategy(),
        # GenerateJsonWithoutFileStrategy(),
        GenerateJsonWithFileStrategy(),
    ]

    runner = StrategyRunner(client)
    await runner.run_all(strategies)


if __name__ == "__main__":
    asyncio.run(main())
