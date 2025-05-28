from pydantic import BaseModel, Field


class OllamaChat(BaseModel):
    model: str = Field(
        description = "Model to use for chatting",
        examples = ["deepseek-r1", "llama3.1"]
    )
    content: str = Field(
            description = "Content of the message",
            examples = ["Why is the sky blue?", "What is the meaning of life?"]
                        )