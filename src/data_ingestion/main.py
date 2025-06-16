import asyncio
from .financial_news import FinancialNewsIngestion
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
            print("1. No news articles in the last hour")
            print("2. API rate limit reached")
            print("3. API key issues")
        pprint(news_data)
        
        # Save the results to a JSON file for inspection
        with open('news_data.json', 'w') as f:
            json.dump(news_data, f, indent=2)
        print("\nData has been saved to 'news_data.json'")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main()) 