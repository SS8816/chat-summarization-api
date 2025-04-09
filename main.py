# main.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_indexes
from routes import chats, users
from sockets import router as websocket_router

app = FastAPI(
    title="Chat Summarization and Insights API",
    description="This API stores chat messages, retrieves conversations, and generates summaries & insights using an LLM.",
    version="2.0.0"
)

# Enable CORS for all origins (helpful when integrating with the Streamlit UI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register REST API routers
app.include_router(chats.router)
app.include_router(users.router)

# Register WebSocket router
app.include_router(websocket_router)

@app.on_event("startup")
async def startup_event():
    await create_indexes()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
