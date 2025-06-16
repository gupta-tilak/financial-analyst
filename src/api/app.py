"""Simple FastAPI application"""

from fastapi import FastAPI
from src.analysis.investment_analyzer import InvestmentAnalyzer

def create_app():
    app = FastAPI(title="Financial Market Analyst", version="1.0.0")
    
    @app.get("/")
    def root():
        return {"message": "Financial Market Analyst API"}
    
    @app.get("/analyze/{ticker}")
    def analyze_stock(ticker: str):
        analyzer = InvestmentAnalyzer()
        result = analyzer.analyze_stock(ticker.upper())
        return result
    
    @app.get("/health")
    def health_check():
        return {"status": "healthy"}
    
    return app
