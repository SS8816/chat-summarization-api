# services/llm.py
from nltk.tokenize import sent_tokenize as original_sent_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
import nltk.tokenize
nltk.tokenize.sent_tokenize = original_sent_tokenize
import os
from typing import List
from models import ChatMessage, ConversationInsights
from transformers import pipeline
import nltk
from pathlib import Path
import traceback

# NEW: KeyBERT for better keyword extraction
from keybert import KeyBERT

nltk_data_path = str(Path.home() / "AppData" / "Roaming" / "nltk_data")
if nltk_data_path not in nltk.data.path:
    nltk.data.path.append(nltk_data_path)

# Ensure required resources are downloaded
nltk.download("punkt", download_dir=nltk_data_path)
nltk.download("stopwords", download_dir=nltk_data_path)

# Initialize Hugging Face pipelines once (this can take some time on first run)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", revision="main")
sentiment_analyzer = pipeline("sentiment-analysis")

# Initialize KeyBERT once
kw_model = KeyBERT()

def generate_summary(conversation: List[ChatMessage]) -> str:
    """
    Generates a summary of the conversation using a pre-trained summarization model.
    """
    # Concatenate the conversation messages (space-separated for summarizer)
    conversation_text = "\n".join([f"{chat.user_id}: {chat.message}" for chat in conversation])

    # The summarizer input length is limited: if conversation_text is too long, we may need to truncate or chunk it.
    # For simplicity, we'll truncate here:
    max_input_length = 1024  # BART typically supports up to 1024 tokens (approx.)
    if len(conversation_text) > max_input_length:
        conversation_text = conversation_text[:max_input_length]

    try:
        # Generate summary; adjust max_length and min_length as needed.
        summary_output = summarizer(conversation_text, max_length=150, min_length=40, do_sample=False)
        summary = summary_output[0]["summary_text"]
    except Exception as e:
        summary = f"Error generating summary: {str(e)}"
    return summary

def extract_insights(conversation: List[ChatMessage]) -> ConversationInsights:
    """
    Extracts conversation insights including overall sentiment and top keywords.
    Uses Hugging Face sentiment analysis for sentiment and KeyBERT for keywords.
    """
    # Concatenate conversation messages
    conversation_text = " ".join([chat.message for chat in conversation])


    # --- Sentiment Analysis using Hugging Face ---
    try:
        sentiments = sentiment_analyzer(conversation_text)
        sentiment = sentiments[0]['label'] if sentiments else "Unknown"
    except Exception as e:
        sentiment = f"Error: {str(e)}"

    # --- Keyword Extraction using KeyBERT ---
    try:
        keywords = [kw[0] for kw in kw_model.extract_keywords(conversation_text, top_n=3)]
    except Exception as e:
        keywords = [f"Error: {traceback.format_exc()}"]

    return ConversationInsights(sentiment=sentiment, keywords=keywords)
