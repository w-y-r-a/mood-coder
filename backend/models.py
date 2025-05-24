from pydantic import BaseModel, Field

class Setup(BaseModel):
    MONGO_URI: str = Field()
    MONGO_DB: str = Field()
    BINDING_KEY: str = Field()