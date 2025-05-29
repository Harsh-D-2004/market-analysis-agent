import requests
from dotenv import load_dotenv
import os



load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def resoning_response(query):

    prompt = f"""
You are a financial reasoning assistant. Your job is to answer only questions that involve general financial concepts, explanations, or reasoning about markets and stocks. You do not have access to real-time or historical data.

Respond to the following user query in short with accurate, professional reasoning

User Query:
{query}
"""

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=data)
    response = response.json()
    result = response['candidates'][0]['content']['parts'][0]['text']
    result = result.strip().replace("\n", "")
    print(result)

    return result