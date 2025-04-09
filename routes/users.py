# routes/users.py
from fastapi import APIRouter, Query
from models import ChatMessage, PagedChats
from database import chat_collection
from typing import List

router = APIRouter()

@router.get("/users/{user_id}/chats", summary="Get User's Chat History", response_model=PagedChats)
async def get_user_chats(user_id: str, page: int = Query(1, ge=1), limit: int = Query(10, ge=1)):
    skip = (page - 1) * limit
    chats = []
    cursor = chat_collection.find({"user_id": user_id}).sort("timestamp", -1).skip(skip).limit(limit)
    async for chat in cursor:
        chats.append(ChatMessage(**chat))
    total = await chat_collection.count_documents({"user_id": user_id})
    return PagedChats(chats=chats, page=page, limit=limit, total=total)
