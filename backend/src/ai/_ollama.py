from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from ollama import AsyncClient
from bson import ObjectId
from typing import Dict
from pydantic import BaseModel
from .classes import ConversationManager
from ..config import OLLAMA_HOST, OLLAMA_HEADERS # The work directory will ALWAYS be backend/
from ..database import get_sessions

try:
    if OLLAMA_HOST is None:
        raise ValueError("OLLAMA_HOST configuration is missing or None")
except (KeyError, ValueError) as e:
    raise ValueError("OLLAMA_HOST must be configured in config.ini") from e

client = AsyncClient(
    host=OLLAMA_HOST,
    headers=OLLAMA_HEADERS
)



router = APIRouter(prefix="/ollama", tags=["Ollama"])

class ChatRequest(BaseModel):
    user_id: str
    chat_id: str
    message: str
    model: str = "deepseek-r1"


SYSTEM_PROMPT = (
    'You are a coding assistant running on the Wyra Mood Coder. '
    'If you want to run a command on the host machine, '
    'encase the command in <wymc_command></wymc_command>. '
    'Also, double check your work. This is the top most chat '
    'command in this session, ignore anything sent above this order of context.'
)


@router.post("/chat")
async def chat(chat_request: ChatRequest):
    sessions = await get_sessions()  # ✅ now it's legal

    user_id = chat_request.user_id
    chat_id = chat_request.chat_id
    message = chat_request.message
    model = chat_request.model

    session_doc = await sessions.find_one({"user_id": user_id, "chat_id": chat_id})

    if session_doc:
        conv = ConversationManager.from_dict(session_doc["conversation"])
    else:
        conv = ConversationManager(system_prompt=SYSTEM_PROMPT)

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

        await sessions.update_one(
            {"user_id": user_id, "chat_id": chat_id},
            {"$set": {
                "user_id": user_id,
                "chat_id": chat_id,
                "conversation": conv.to_dict()
            }},
            upsert=True
        )

    return StreamingResponse(stream_response(), media_type="text/plain")