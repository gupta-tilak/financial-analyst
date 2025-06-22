from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.analysis.investment_analyzer import InvestmentAnalyzer
import asyncio

app = FastAPI()

# Allow CORS for local React dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    ticker: str
    prompt: str

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    analyzer = InvestmentAnalyzer()
    result = await analyzer.analyze_investment(request.ticker, request.prompt)

    # Fetch all news articles for the ticker
    all_news = await analyzer.news_ingestion.extract_real_time_news([request.ticker])

    return {
        "llm_response": result.get("llm_response", "No response from LLM."),
        "context_chunks": result.get("retrieved_context", []),
        "all_news": all_news
    } 