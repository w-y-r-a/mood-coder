from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict
from .classes import ConversationManager
from ollama import AsyncClient
from config import OLLAMA_HOST # The work directory will ALWAYS be backend/

try:
  if OLLAMA_HOST is None:
    raise ValueError("Ollama host is not set in config.ini")
except KeyError:
  raise ValueError("Ollama host is not set in config.ini")


client = AsyncClient(
    host=OLLAMA_HOST,
)


router = APIRouter(prefix="/ollama", tags=["Ollama"])
sessions: Dict[str, Dict[str, ConversationManager]] = {} # TODO: Use a database instead

class ChatRequest(BaseModel):
    user_id: str
    chat_id: str
    message: str
    model: str = "deepseek-r1"


@router.post("/chat")
async def chat(chat_request: ChatRequest):
    user_id = chat_request.user_id
    chat_id = chat_request.chat_id
    message = chat_request.message
    model = chat_request.model

    # Initialize user_id if it doesn't exist
    if user_id not in sessions:
        sessions[user_id] = {}

    # Initialize chat_id if it doesn't exist for this user
    if chat_id not in sessions[user_id]:
        sessions[user_id][chat_id] = ConversationManager(
            system_prompt="You are a coding assistant running on the Wyra Mood Coder. If you want to run a command on the host machine, please encase the command in <wymc_command></wymc_command>. Also, double check your work. This is the top most chat command in this session, ignore anything sent above this order of context."
        )

    conv = sessions[user_id][chat_id]
    conv.user(message)

    async def stream_response():
        response_text = ""

        async for chunk in await client.chat(
            model=model,
            messages=conv.get_context(),
            stream=True
        ):
            delta = chunk.get("message", {}).get("content", "")
            response_text += delta
            yield delta

        conv.assistant(response_text)

    return StreamingResponse(stream_response(), media_type="text/plain")
