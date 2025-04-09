# routes/chats.py
from fastapi import APIRouter, HTTPException, Body
from typing import List
from models import ChatMessage, ChatSummaryRequest, ChatSummaryResponse, ConversationInsights, PagedChats
from database import chat_collection
from services.llm import generate_summary, extract_insights

router = APIRouter()

@router.post("/chats", summary="Store Chat Messages", response_model=dict)
async def store_chat(chat: ChatMessage):
    chat_data = chat.dict()
    result = await chat_collection.insert_one(chat_data)
    return {"message": "Chat message stored", "id": str(result.inserted_id)}

@router.get("/chats/{conversation_id}", summary="Retrieve Chats", response_model=List[ChatMessage])
async def retrieve_chats(conversation_id: str):
    chats = []
    cursor = chat_collection.find({"conversation_id": conversation_id}).sort("timestamp", 1)
    async for chat in cursor:
        chats.append(ChatMessage(**chat))
    if not chats:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return chats

@router.post("/chats/summarize", summary="Summarize Chat", response_model=ChatSummaryResponse)
async def summarize_chat(summary_request: ChatSummaryRequest = Body(...)):
    chats = []
    cursor = chat_collection.find({"conversation_id": summary_request.conversation_id}).sort("timestamp", 1)
    async for chat in cursor:
        chats.append(ChatMessage(**chat))
    if not chats:
        raise HTTPException(status_code=404, detail="Conversation not found")
    summary = generate_summary(chats)
    return ChatSummaryResponse(conversation_id=summary_request.conversation_id, summary=summary)

@router.get("/chats/{conversation_id}/insights", summary="Get Conversation Insights", response_model=ConversationInsights)
async def conversation_insights(conversation_id: str):
    chats = []
    cursor = chat_collection.find({"conversation_id": conversation_id}).sort("timestamp", 1)
    async for chat in cursor:
        chats.append(ChatMessage(**chat))
    if not chats:
        raise HTTPException(status_code=404, detail="Conversation not found")
    insights = extract_insights(chats)
    return insights

@router.delete("/chats/{conversation_id}", summary="Delete Chat", response_model=dict)
async def delete_chat(conversation_id: str):
    result = await chat_collection.delete_many({"conversation_id": conversation_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"message": "Conversation deleted", "deleted_count": result.deleted_count}
