"""Simple investment analysis using collected data"""

import pandas as pd
from src.vector_db.database import VectorDatabase
from src.analysis.sentiment_analyzer import SentimentAnalyzer
import config.settings as config

class InvestmentAnalyzer:
    def __init__(self):
        self.vector_db = VectorDatabase()
        self.sentiment_analyzer = SentimentAnalyzer()
        
    def analyze_stock(self, ticker):
        """Perform simple investment analysis"""
        print(f"🔍 Analyzing {ticker}...")
        
        # Get relevant news
        news_data = self.get_stock_news(ticker)
        
        # Analyze sentiment
        sentiment_score = self.sentiment_analyzer.analyze_ticker_sentiment(ticker)
        
        # Get financial metrics (simplified)
        financial_health = self.assess_financial_health(ticker)
        
        # Generate recommendation
        recommendation = self.generate_recommendation(
            sentiment_score, financial_health
        )
        
        return {
            "ticker": ticker,
            "sentiment_score": sentiment_score,
            "financial_health": financial_health,
            "recommendation": recommendation,
            "confidence": self.calculate_confidence(sentiment_score, financial_health)
        }
        
    def generate_recommendation(self, sentiment, financial_health):
        """Simple rule-based recommendation"""
        if sentiment > 0.6 and financial_health > 0.7:
            return "BUY"
        elif sentiment < 0.4 or financial_health < 0.3:
            return "SELL"
        else:
            return "HOLD"
            
    def calculate_confidence(self, sentiment, financial_health):
        """Calculate confidence score"""
        return (abs(sentiment - 0.5) + abs(financial_health - 0.5)) / 1.0
