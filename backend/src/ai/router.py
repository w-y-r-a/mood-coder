from fastapi import APIRouter
from typing import List, Dict
from ..main.utils import verify_key

router = APIRouter(prefix='/chats')

@router.get('/', response_model=List[Dict])
async def get_chats() -> List[Dict]:
    """
    Retrieve a list of all chat sessions.

    Returns:
        List[Dict]: A list of chat sessions, where each session contains:
            - chat_id: Unique identifier for the chat
            - user_id: ID of the user who owns the chat
            - created_at: Timestamp of chat creation
            - last_message: Timestamp of the last message
            - title: Chat title or first message preview
    """
    # TODO: Implement chat session retrieval from database
    # - Query the sessions collection
    # - Filter and format chat metadata
    # - Sort by latest activity
    # - Return formatted chat list
    return []
