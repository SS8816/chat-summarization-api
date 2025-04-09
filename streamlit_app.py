# streamlit_app.py
import streamlit as st
import requests
import json
import asyncio
import websockets

API_URL = "http://localhost:8000"

st.title("Chat Summarization and Insights")

# Sidebar options to select functionality
option = st.sidebar.selectbox("Choose Action", 
                              ["Send Chat Message", "View Conversation", "Get Conversation Summary", "Get Conversation Insights"])

if option == "Send Chat Message":
    st.header("Send Chat Message")
    conversation_id = st.text_input("Conversation ID")
    user_id = st.text_input("User ID")
    message = st.text_area("Message")
    if st.button("Send"):
        data = {
            "conversation_id": conversation_id,
            "user_id": user_id,
            "message": message
        }
        response = requests.post(f"{API_URL}/chats", json=data)
        if response.status_code == 200:
            st.success("Message sent!")
        else:
            st.error("Error sending message.")

elif option == "View Conversation":
    st.header("View Conversation")
    conversation_id = st.text_input("Conversation ID to view")
    if st.button("View"):
        response = requests.get(f"{API_URL}/chats/{conversation_id}")
        if response.status_code == 200:
            chats = response.json()
            for chat in chats:
                st.write(f"{chat['timestamp']} - {chat['user_id']}: {chat['message']}")
        else:
            st.error("Conversation not found.")

elif option == "Get Conversation Summary":
    st.header("Get Conversation Summary")
    conversation_id = st.text_input("Conversation ID to summarize")
    if st.button("Summarize"):
        data = {"conversation_id": conversation_id}
        response = requests.post(f"{API_URL}/chats/summarize", json=data)
        if response.status_code == 200:
            summary = response.json()["summary"]
            st.write("Summary:")
            st.write(summary)
        else:
            st.error("Conversation not found.")

elif option == "Get Conversation Insights":
    st.header("Get Conversation Insights")
    conversation_id = st.text_input("Conversation ID for insights")
    if st.button("Get Insights"):
        response = requests.get(f"{API_URL}/chats/{conversation_id}/insights")
        if response.status_code == 200:
            insights = response.json()
            st.write("Sentiment:", insights["sentiment"])
            st.write("Keywords:", ", ".join(insights["keywords"]))
        else:
            st.error("Conversation not found.")

st.markdown("---")
st.write("This Streamlit app interacts with the FastAPI backend.")

# Section for real-time summarization using WebSockets
st.header("Real-Time Summarization (WebSocket)")
conversation_id_ws = st.text_input("Conversation ID for real-time summarization", key="ws_convo")
message_ws = st.text_area("Type message for WebSocket simulation", key="ws_message")

if st.button("Send via WebSocket", key="ws_send"):
    async def websocket_client():
        uri = f"ws://localhost:8000/ws/summarize/{conversation_id_ws}"
        async with websockets.connect(uri) as websocket:
            # Send the chat message as JSON
            await websocket.send(json.dumps({
                "conversation_id": conversation_id_ws,
                "user_id": "ws_user",
                "message": message_ws
            }))
            # Receive and display the updated summary
            summary = await websocket.recv()
            st.write("Real-time summary:", summary)
    asyncio.run(websocket_client())
