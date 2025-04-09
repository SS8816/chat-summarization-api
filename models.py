# models.py
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    conversation_id: str = Field(..., description="Unique conversation identifier")
    user_id: str = Field(..., description="User identifier who sent the message")
    message: str = Field(..., description="Chat message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the message")

class ChatSummaryRequest(BaseModel):
    conversation_id: str = Field(..., description="Unique conversation identifier for summarization")

class ChatSummaryResponse(BaseModel):
    conversation_id: str
    summary: str

class PagedChats(BaseModel):
    chats: List[ChatMessage]
    page: int
    limit: int
    total: int

class ConversationInsights(BaseModel):
    sentiment: str
    keywords: List[str]
