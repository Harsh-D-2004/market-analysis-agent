import requests
from dotenv import load_dotenv
import os
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import re
import string


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("finance-agent")

model = SentenceTransformer("all-MiniLM-L6-v2")  


def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_context(query  ,threshold = 0.2):
    preprocessed_query = preprocess(query)
    embedded_query = model.encode([preprocessed_query])[0].tolist()
    results = index.query(vector = embedded_query, top_k=6, include_metadata=True)

    matches = results.get("matches", [])
    
    confident_matches = [match for match in matches if match.get("score", 0) >= threshold]

    if not confident_matches:
        return -1

    return confident_matches

def llm_analysis(query):

    context = get_context(query)

    if context == -1:
        return "We currently dont have enough data to provide a response. Please try again later."

    prompt = f"""
You are a senior financial analyst.

Using the context below, provide an short insightful summary like a portfolio manager would, highlighting:
- Sector performance for stocks present in query
- Price percentage changes for stocks present in query
- Analysis of stocks present in query 

Context:
{context}

Query:
{query}

Your analysis should not more than three sentences, and should be clear and professional, with numbers and relevant financial insight.
Return plain strings only.
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