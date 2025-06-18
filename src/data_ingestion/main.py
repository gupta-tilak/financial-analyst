import sys
import os
# Ensure the project root is in sys.path for direct script execution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.data_ingestion.financial_news import FinancialNewsIngestion

import asyncio
import json
from pprint import pprint

async def main():
    # Initialize the news ingestion class
    news_ingestion = FinancialNewsIngestion()
    
    # Example tickers to fetch news for
    test_tickers = ['AAPL', 'MSFT', 'GOOGL']
    
    try:
        print(f"Fetching news for tickers: {test_tickers}")
        # Fetch news data
        news_data = await news_ingestion.extract_real_time_news(test_tickers)
        
        # Print the results in a readable format
        print("\nFetched News Data:")
        print("=" * 80)
        
        if not news_data:
            print("No news data was returned. This could be because:")
            print("1. No news articles found")
            print("2. API rate limit reached")
            print("3. API key issues")
        else:
            print(f"Total articles collected: {len(news_data)}")
            print("\nSample articles:")
            print("-" * 80)
            
            # Show first 3 articles as samples
            for i, article in enumerate(news_data[:3]):
                print(f"\nArticle {i+1}:")
                print(f"  Title: {article.get('title', 'N/A')}")
                print(f"  Source: {article.get('source', 'N/A')}")
                print(f"  Author: {article.get('author', 'N/A')}")
                print(f"  Published: {article.get('published_utc', 'N/A')}")
                print(f"  Tickers: {article.get('ticker', [])}")
                print(f"  Keywords: {article.get('keywords', [])[:3]}...")  # Show first 3 keywords
                print(f"  URL: {article.get('article_url', 'N/A')}")
            
            if len(news_data) > 3:
                print(f"\n... and {len(news_data) - 3} more articles")
        
        # Save the results to a JSON file for inspection
        with open('news_data.json', 'w') as f:
            json.dump(news_data, f, indent=2)
        print(f"\n✅ All {len(news_data)} articles have been saved to 'news_data.json'")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())