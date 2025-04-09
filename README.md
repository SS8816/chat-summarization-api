# Chat Summarization and Insights API

## Setup Instructions

1. **Clone the repository.**
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  
    
3. Install dependencies:
    pip install -r requirements.txt

4. Create a .env file with your OpenAI API key and MongoDB
connection:
    OPENAI_API_KEY=your_openai_api_key_here
    MONGO_DETAILS=mongodb://localhost:27017

5. Run the FastAPI server:
    uvicorn main:app --reload

6. Run the Streamlit app (in a separate terminal):
    streamlit run streamlit_app.py

7. API Documentation
Access the interactive API docs at http://localhost:8000/docs.


8. Docker - To build and run with Docker:
    docker build -t chat-api .
    docker run -d -p 8000:8000 chat-api
