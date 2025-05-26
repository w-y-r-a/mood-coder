from pydantic import BaseModel, Field

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