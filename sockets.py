# sockets.py
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from models import ChatMessage
from services.llm import generate_summary

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_summary(self, summary: str, websocket: WebSocket):
        await websocket.send_text(summary)

manager = ConnectionManager()

@router.websocket("/ws/summarize/{conversation_id}")
async def websocket_summary(websocket: WebSocket, conversation_id: str):
    await manager.connect(websocket)
    conversation = []  # In-memory conversation for WebSocket session
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            # Create a ChatMessage instance; the timestamp is auto-generated.
            chat = ChatMessage(**message_data)
            conversation.append(chat)
            if len(conversation) % 1 == 0:
                summary = generate_summary(conversation)
                await manager.send_summary(f"Summary: {summary}", websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
