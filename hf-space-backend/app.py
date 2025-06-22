from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from src.analysis.investment_analyzer import InvestmentAnalyzer

app = FastAPI()
analyzer = InvestmentAnalyzer()

class AnalyzeRequest(BaseModel):
    ticker: str
    question: str

@app.post("/analyze_investment")
async def analyze_investment(req: AnalyzeRequest):
    result = await analyzer.analyze_investment(req.ticker, req.question)
    return result 