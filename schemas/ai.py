from pydantic import BaseModel, Field


class AIChatMessage(BaseModel):
    role: str = Field(..., pattern="^(system|user|assistant)$")
    content: str


class AIChatRequest(BaseModel):
    messages: list[AIChatMessage]
    model: str | None = None
