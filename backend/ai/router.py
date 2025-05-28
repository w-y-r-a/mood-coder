from fastapi import APIRouter
from utils import verify_key

router = APIRouter(prefix='/chats')

@router.get('/')
async def get_chats():
