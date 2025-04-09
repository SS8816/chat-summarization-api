# Chat Summarization & Insights API

A FastAPI-based backend service for real-time chat ingestion, LLM-powered summarization, sentiment analysis, and keyword extraction. Built for high-performance CRUD operations with full Docker support.

---

##  Features

- **Store Chats**: Real-time ingestion of chat messages into a MongoDB database.
- **Retrieve Conversations**: Filter by conversation ID, user ID, date, and more.
- **Summarize Conversations**: Generate concise summaries using HuggingFace’s `facebook/bart-large-cnn` model.
- **Get Insights**: Analyze overall sentiment and extract top keywords with `transformers` + RAKE.
- **Optimized CRUD**: Built to handle heavy loads with efficient DB queries.
- **Streamlit UI** *(Bonus)*: (WIP) Chat interface with LLM-powered summarization.
- **Dockerized**: Containerized and production-ready.

---

##  Tech Stack

- **Backend**: FastAPI
- **Database**: MongoDB (via `motor` async client)
- **NLP**: Hugging Face Transformers (`bart-large-cnn`, `sentiment-analysis`)
- **Keyword Extraction**: RAKE via `rake-nltk`
- **Containerization**: Docker

---

##  API Endpoints

###  POST `/chats`
Store a chat message.

## Project Structure
chat-summarization-api/
│
├── app/                  # FastAPI app logic
│   ├── main.py
│   ├── models.py
│   ├── services/
│   │   └── llm.py        # LLM summarization & insights logic
│   └── database.py       # MongoDB connection
│
├── requirements.txt
├── Dockerfile
└── README.md

## Local Development
1. Clone the Repo
git clone https://github.com/SS8816/chat-summarization-api.git
cd chat-summarization-api
2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # On Windows
3. Install Dependencies
pip install -r requirements.txt
4. Run the API
uvicorn main:app --reload
5. Run the streamlit UI
streamlit run streamlit_app.py

## Environment Variables
Make sure to set:

MONGODB_URL: Your MongoDB connection string

You can use a .env file or set it in your terminal/session.

## License
MIT License. 
