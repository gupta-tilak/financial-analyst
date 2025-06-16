"""Simple financial news collection"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import config.settings as config

class NewsCollector:
    def __init__(self):
        self.news_data = []
        
    def collect_recent_news(self, tickers=None):
        """Collect recent financial news"""
        if tickers is None:
            tickers = config.DEMO_TICKERS
            
        print(f"📰 Collecting news for {tickers}")
        
        # Simple news collection (replace with actual API calls)
        for ticker in tickers:
            # Demo data - replace with real API calls
            news_items = self.get_demo_news(ticker)
            self.news_data.extend(news_items)
            
        # Save to CSV
        df = pd.DataFrame(self.news_data)
        df.to_csv(config.RAW_DATA_DIR / "financial_news.csv", index=False)
        print(f"✅ Saved {len(self.news_data)} news articles")
        
    def get_demo_news(self, ticker):
        """Generate demo news data"""
        return [
            {
                "ticker": ticker,
                "title": f"{ticker} Reports Strong Q4 Earnings",
                "content": f"{ticker} exceeded analyst expectations with strong quarterly results...",
                "published_date": datetime.now().isoformat(),
                "sentiment": "positive"
            },
            {
                "ticker": ticker,
                "title": f"Market Volatility Affects {ticker} Trading",
                "content": f"Recent market conditions have impacted {ticker} stock performance...",
                "published_date": (datetime.now() - timedelta(days=1)).isoformat(),
                "sentiment": "neutral"
            }
        ]
