import yfinance as yf
import re
import string
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os


load_dotenv()

tickers = ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL", "NFLX", "GOOG", "INTC", "IBM" , "INFY", "WIT", "SONY", "NTES" , "JPM", "BAC", "HSBC"]

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("finance-agent")

model = SentenceTransformer("all-MiniLM-L6-v2")  

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

async def upsert_vector(texts : list , ids : list):
    embeddings = model.encode(texts).tolist()

    vectors = [
        {"id": str(idx), "values": emb, "metadata": {"text": text}}
        for idx, (emb, text) in enumerate(zip(embeddings, texts))
    ]

    index.upsert(vectors)

def clear_pinecone_index():
    index.delete(delete_all=True)

async def yfinance_scraping():

    result_text = []

    clear_pinecone_index()

    for ticker in tickers:
        ticker = ticker.upper()
        info = yf.Ticker(ticker)
        Sector = info.info.get("sector", "N/A")
        Region = info.info.get("region", "N/A")
        prices = yf.download(ticker, period="2d")

        # result_text = []

        for date in prices.index:

            open_price = float(prices.loc[date, 'Open'].iloc[0])
            close_price = float(prices.loc[date , 'Close'].iloc[0])
            volume = float(prices.loc[date , 'Volume'].iloc[0])

            summary = (
                f"In {Sector} in {Region}, "
                f"On {date}, {ticker} opened at ${open_price:.2f}, "
                f"closed at ${close_price:.2f}, with a trading volume of {int(volume):,} shares."
            )
            result_text.append(preprocess(summary))
    
    # print(result_text)
    # print(len(result_text))

    await upsert_vector(result_text , range(len(result_text)))

    return result_text