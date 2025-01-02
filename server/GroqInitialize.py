import os
import logging
from flask import request, jsonify
from dotenv import load_dotenv
from langdetect import detect
from groq import Groq
from groq._base_client import SyncHttpxClientWrapper

# Load environment variables
load_dotenv()

# Validate environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY is not set in the environment variables.")

# Initialize Groq client with custom HTTP client
http_client = SyncHttpxClientWrapper()
client = Groq(api_key=GROQ_API_KEY, http_client=http_client)

# Groq parameters
#DEFAULT_MODEL = "llama-3.1-70b-versatile"
DEFAULT_MODEL = "llama-3.2-90b-vision-preview"
DEFAULT_TEMPERATURE = 1
DEFAULT_MAX_TOKENS = 1024

PROMPT = """
Question: {query}
You are a data analyst responsible for extracting insights and generating graphs for the provided CSV file."""

def initialize_groq_api():
    try:
        data = request.get_json()
        messages = data.get('messages', [])

        # Check if messages are empty or contain no content
        if not messages or all(not msg.get("content") for msg in messages):
            return jsonify({
                "message": "How can I help you?",
                "tokens_used": 0
            }), 200

        full_messages = [{"role": "system", "content": PROMPT}]

        # Process each message, detect language, and prepare for Groq API
        for msg in messages:
            if "content" in msg and msg["content"].strip():
                user_language = detect(msg["content"])
                prompt_with_language = f"{PROMPT}\nRespond in {user_language}."
                full_messages[0]["content"] = prompt_with_language
                msg["role"] = "user"
                full_messages.append(msg)

        # Send request to the Groq API
        response = client.chat.completions.create(
            messages=full_messages,
            model=DEFAULT_MODEL,
            temperature=DEFAULT_TEMPERATURE,
            max_tokens=DEFAULT_MAX_TOKENS
        )
        assistant_message = response.choices[0].message.content

        return jsonify({
            "message": assistant_message,
            "tokens_used": response.usage.total_tokens
        }), 200

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
