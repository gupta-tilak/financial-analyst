# Financial News Data Pipeline
import asyncio
import time
import random
from datetime import datetime, timedelta
import pandas as pd
from typing import List, Dict
from polygon import RESTClient
from polygon.rest.models import TickerNews
from .config import POLYGON_API_KEY, POLYGON_RATE_LIMIT

class FinancialNewsIngestion:
    def __init__(self):
        self.client = RESTClient(POLYGON_API_KEY)
        # Rate limiting settings from config
        self.requests_per_minute = POLYGON_RATE_LIMIT['requests_per_minute']
        self.min_delay = 60 / self.requests_per_minute  # Minimum seconds between requests
        self.max_retries = POLYGON_RATE_LIMIT['max_retries']
        self.base_delay = POLYGON_RATE_LIMIT['base_delay']
        self.enable_jitter = POLYGON_RATE_LIMIT['enable_jitter']
        self.last_request_time = 0
    
    def _rate_limit_delay(self):
        """Implement rate limiting to avoid 429 errors"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_delay:
            sleep_time = self.min_delay - time_since_last
            # Add some jitter to avoid thundering herd
            if self.enable_jitter:
                jitter = random.uniform(0, 2)
                total_sleep = sleep_time + jitter
            else:
                total_sleep = sleep_time
            print(f"Rate limiting: waiting {total_sleep:.1f} seconds...")
            time.sleep(total_sleep)
        
        self.last_request_time = time.time()
    
    async def _fetch_news_with_retry(self, ticker: str, retry_count: int = 0) -> List[Dict]:
        """Fetch news with exponential backoff retry logic"""
        try:
            self._rate_limit_delay()
            
            # Use the official Polygon SDK to fetch news
            news_items = []
            for news_item in self.client.list_ticker_news(
                ticker=ticker,
                order="desc",  # Get most recent first
                limit=50,
                sort="published_utc"
            ):
                news_items.append(news_item)
                if len(news_items) >= 50:  # Limit to 50 articles per ticker
                    break
            
            print(f"Found {len(news_items)} articles for {ticker}")
            
            # Convert TickerNews objects to dictionaries
            news_data = []
            for item in news_items:
                if isinstance(item, TickerNews):
                    news_data.append({
                        'id': item.id,
                        'publisher': {
                            'name': item.publisher.name if item.publisher else None,
                            'homepage_url': item.publisher.homepage_url if item.publisher else None,
                            'logo_url': item.publisher.logo_url if item.publisher else None,
                            'favicon_url': item.publisher.favicon_url if item.publisher else None
                        },
                        'title': item.title,
                        'author': item.author,
                        'published_utc': item.published_utc,
                        'article_url': item.article_url,
                        'tickers': item.tickers,
                        'image_url': item.image_url,
                        'description': item.description,
                        'keywords': item.keywords
                    })
            
            return news_data
            
        except Exception as e:
            error_msg = str(e).lower()
            
            # Check if it's a rate limit error
            if '429' in error_msg or 'too many' in error_msg or 'rate limit' in error_msg:
                if retry_count < self.max_retries:
                    # Exponential backoff: wait 2^retry_count * base_delay seconds
                    delay = (2 ** retry_count) * self.base_delay
                    print(f"Rate limit hit for {ticker}. Retrying in {delay} seconds... (attempt {retry_count + 1}/{self.max_retries})")
                    time.sleep(delay)
                    return await self._fetch_news_with_retry(ticker, retry_count + 1)
                else:
                    print(f"Max retries exceeded for {ticker}. Skipping this ticker.")
                    return []
            else:
                # For other errors, just log and return empty list
                print(f"Error fetching news for {ticker}: {str(e)}")
                return []
    
    async def extract_real_time_news(self, tickers: List[str]) -> List[Dict]:
        """Real-time news extraction using Polygon SDK with rate limiting"""
        news_data = []
        
        print(f"Starting news extraction for {len(tickers)} tickers with rate limiting...")
        print(f"Rate limit: {self.requests_per_minute} requests per minute (min {self.min_delay:.1f}s between requests)")
        
        for i, ticker in enumerate(tickers):
            print(f"\nFetching news for {ticker} ({i+1}/{len(tickers)})...")
            
            ticker_news = await self._fetch_news_with_retry(ticker)
            news_data.extend(ticker_news)
        
        print(f"\nTotal articles collected: {len(news_data)}")
        
        # Transform the data and convert to list of dictionaries
        df = self.transform_news_data(news_data)
        if df.empty:
            return []
        return df.to_dict('records')
    
    def transform_news_data(self, raw_data: List[Dict]) -> pd.DataFrame:
        """Data transformation as per ETL process"""
        transformed_data = []
        
        for article in raw_data:
            transformed_article = {
                'article_id': article.get('id'),
                'title': article.get('title'),
                'description': article.get('description'),
                'content': article.get('description', ''),  # Using description as content since content field is not available
                'published_utc': article.get('published_utc'),
                'ticker': article.get('tickers', []),
                'sentiment_score': None,  # To be filled by sentiment analysis
                'keywords': article.get('keywords', []),
                'source': article.get('publisher', {}).get('name'),
                'author': article.get('author'),
                'article_url': article.get('article_url'),
                'image_url': article.get('image_url'),
                'ingestion_timestamp': datetime.now().isoformat()
            }
            transformed_data.append(transformed_article)
        
        return pd.DataFrame(transformed_data)