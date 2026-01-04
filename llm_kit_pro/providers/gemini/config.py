from pydantic import BaseModel, Field


class GeminiConfig(BaseModel):
    api_key: str = Field(..., description="Gemini API key")
    model: str = Field(..., description="Gemini model to use")
    temperature: float = Field(default=0.2)
