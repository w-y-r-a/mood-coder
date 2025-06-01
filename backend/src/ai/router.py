from fastapi import APIRouter
from ..main.utils import verify_key

router = APIRouter(prefix='/chats')

@router.get('/')
async def get_chats():
    pass