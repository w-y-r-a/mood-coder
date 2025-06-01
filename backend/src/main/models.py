from pydantic import BaseModel, Field
from typing import Optional

class Setup(BaseModel):
        MONGO_URI: str = Field(
                description = "MongoDB connection URI",
            pattern = r'^mongodb(\+srv)?://.*',
            examples = ["mongodb://localhost:27017", "mongodb+srv://cluster.mongodb.net"]
                            )
        MONGO_DB: str = Field(
                description = "MongoDB database name",
            min_length = 1,
            max_length = 64,
            pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
                           )
        BINDING_KEY: str = Field(
                description = "API binding key for authentication",
            min_length = 8,
            max_length = 128
                              )
        OLLAMA: bool = Field(
            description = "Whether to use Ollama for chatting. If enabled, also specify OLLAMA_HOST",
            examples = [True, False]
        )
        OLLAMA_HOST: Optional[str] = Field(
            default=None,
            description="Host for Ollama server",
            examples=["http://localhost:11434"]
        )


class OllamaChat(BaseModel):
    model: str = Field(
        description = "Model to use for chatting",
        examples = ["deepseek-r1", "llama3.1"]
    )
    content: str = Field(
            description = "Content of the message",
            examples = ["Why is the sky blue?", "What is the meaning of life?"]
                        )