import requests
from dotenv import load_dotenv
import os
from langchain_core.runnables import RunnableLambda, RunnableBranch
from agents.knowledge_based_retrieval import llm_analysis
from agents.reasoning_response import resoning_response

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def get_query(query):

    prompt = f"""
Classify the following query into one of the following three categories:
1. knowledge_required — if it needs factual or historical company/market data that can be retrieved from a database or index.
2. knowledge_not_required — if it asks for explanations, opinions, or general market principles not tied to a specific stored context.
3. not_related_to_market — if it doesn't relate to financial markets.

Examples:
- "What was AAPL's closing price yesterday?" => knowledge_required
- "Explain what a stock split is" => knowledge_not_required
- "Is the market open today?" => knowledge_not_required
- "Who is the CEO of Microsoft?" => unrelated
- "How does inflation impact markets?" => knowledge_not_required

Now classify this query:
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
    # print(response)
    result = response['candidates'][0]['content']['parts'][0]['text']
    result = result.lower().strip().replace("\n", "")
    print(result)

    return result

def classifier_wrapper(query):
    label =  get_query(query)
    return {"query": query, "label": label}

def get_knowledge_based_response(query):
    result = llm_analysis(query)
    return result

def get_reasoning_response(query):
    result = resoning_response(query)
    return result

def get_default_response(query):
    return "I'm sorry, I don't have the information you're looking for. I can only answer questions that involve markets and stocks"

router = (
    RunnableLambda(classifier_wrapper)
    | RunnableBranch(
        (lambda x: x["label"] == "knowledge_required", 
         RunnableLambda(lambda x: get_knowledge_based_response(x["query"]))),
        
        (lambda x: x["label"] == "knowledge_not_required", 
         RunnableLambda(lambda x: get_reasoning_response(x["query"]))),
        
        (lambda x: x["label"] == "not_related_to_market", 
         RunnableLambda(lambda x: get_default_response(x["query"]))),

        RunnableLambda(lambda x: "Unable to classify query.")
    )
)

def invoke_router(query):
    response = router.invoke(query)
    return response