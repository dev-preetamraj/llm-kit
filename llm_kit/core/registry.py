from typing import Dict, Literal, Type, overload

from llm_kit.core.base import BaseLLMClient
from llm_kit.providers.bedrock.client import BedrockClient
from llm_kit.providers.gemini.client import GeminiClient

# ---------------- runtime registry ----------------

_PROVIDER_REGISTRY: Dict[str, Type[BaseLLMClient]] = {}


def register_provider(name: str, client: Type[BaseLLMClient]) -> None:
    _PROVIDER_REGISTRY[name] = client


# ---------------- typing helpers ----------------

ProviderName = Literal["bedrock", "gemini"]


@overload
def get_provider(name: Literal["bedrock"]) -> Type[BedrockClient]: ...
@overload
def get_provider(name: Literal["gemini"]) -> Type[GeminiClient]: ...


def get_provider(name: ProviderName) -> Type[BaseLLMClient]:
    if name not in _PROVIDER_REGISTRY:
        raise ValueError(f"Provider '{name}' not registered")
    return _PROVIDER_REGISTRY[name]
