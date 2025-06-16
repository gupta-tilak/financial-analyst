# Financial News Data Pipeline
import asyncio
import aiohttp
from datetime import datetime, timedelta
import pandas as pd
from typing import List, Dict
from .config import API_ENDPOINTS, POLYGON_API_KEY

class FinancialNewsIngestion:
    def __init__(self):
        self.news_sources = API_ENDPOINTS
    async def extract_real_time_news(self, tickers: List[str]) -> Dict:
        """Real-time news extraction with streaming processing"""
        news_data = []
        
        for ticker in tickers:
            print(f"\nFetching news for {ticker}...")
            # Real-time processing as described in search results
            async with aiohttp.ClientSession() as session:
                # Format the date in the correct format for Polygon API
                one_hour_ago = (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
                params = {
                    'ticker': ticker,
                    'published_utc.gte': one_hour_ago,
                    'limit': 50,
                    'apikey': POLYGON_API_KEY
                }
                
                print(f"Making API request to {self.news_sources['polygon']}")
                async with session.get(self.news_sources['polygon'], params=params) as response:
                    data = await response.json()
                    print(f"Response status: {response.status}")
                    if response.status != 200:
                        print(f"Error response: {data}")
                    news_data.extend(data.get('results', []))
                    print(f"Found {len(data.get('results', []))} articles for {ticker}")
        
        # Transform the data and convert to dictionary
        df = self.transform_news_data(news_data)
        if df.empty:
            return {}
        return df.to_dict('records')[0] if len(df) > 0 else {}
    
    def transform_news_data(self, raw_data: List[Dict]) -> pd.DataFrame:
        """Data transformation as per ETL process"""
        transformed_data = []
        
        for article in raw_data:
            transformed_article = {
                'article_id': article.get('id'),
                'title': article.get('title'),
                'description': article.get('description'),
                'content': article.get('content', ''),
                'published_utc': article.get('published_utc'),
                'ticker': article.get('tickers', []),
                'sentiment_score': None,  # To be filled by sentiment analysis
                'keywords': article.get('keywords', []),
                'source': article.get('publisher', {}).get('name'),
                'ingestion_timestamp': datetime.now().isoformat()
            }
            transformed_data.append(transformed_article)
        
        return pd.DataFrame(transformed_data)