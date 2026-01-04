from pydantic import BaseModel, Field


class OpenAIConfig(BaseModel):
    api_key: str = Field(..., description="OpenAI API key")
    model: str = Field(..., description="OpenAI model to use")
    temperature: float = Field(default=0.2)
