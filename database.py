# database.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client.chat_db
chat_collection = db.get_collection("chats")

async def create_indexes():
    await chat_collection.create_index("conversation_id")
    await chat_collection.create_index("user_id")
    await chat_collection.create_index("timestamp")
