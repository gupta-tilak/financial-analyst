import pytest
import asyncio
from datetime import datetime, timedelta
from src.data_ingestion.financial_news import FinancialNewsIngestion
import pandas as pd

@pytest.fixture
def news_ingestion():
    return FinancialNewsIngestion()

@pytest.mark.asyncio
async def test_extract_real_time_news(news_ingestion):
    # Test with a single ticker
    tickers = ['AAPL']
    result = await news_ingestion.extract_real_time_news(tickers)
    
    # Verify the result is a dictionary
    assert isinstance(result, dict)
    
    # If we got results, verify the structure
    if result:
        # Verify the result contains expected keys
        assert 'article_id' in result
        assert 'title' in result
        assert 'description' in result
        assert 'content' in result
        assert 'published_utc' in result
        assert 'ticker' in result
        assert 'sentiment_score' in result
        assert 'keywords' in result
        assert 'source' in result
        assert 'ingestion_timestamp' in result

@pytest.mark.asyncio
async def test_extract_real_time_news_multiple_tickers(news_ingestion):
    # Test with multiple tickers
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    result = await news_ingestion.extract_real_time_news(tickers)
    
    # Verify the result is a dictionary
    assert isinstance(result, dict)
    
    # If we got results, verify the structure
    if result:
        # Verify the result contains expected keys
        assert 'article_id' in result
        assert 'title' in result
        assert 'description' in result
        assert 'content' in result
        assert 'published_utc' in result
        assert 'ticker' in result
        assert 'sentiment_score' in result
        assert 'keywords' in result
        assert 'source' in result
        assert 'ingestion_timestamp' in result

@pytest.mark.asyncio
async def test_transform_news_data(news_ingestion):
    # Sample raw data
    raw_data = [{
        'id': '123',
        'title': 'Test Article',
        'description': 'Test Description',
        'content': 'Test Content',
        'published_utc': datetime.now().isoformat(),
        'tickers': ['AAPL'],
        'keywords': ['test', 'news'],
        'publisher': {'name': 'Test Publisher'}
    }]
    
    # Transform the data
    result = news_ingestion.transform_news_data(raw_data)
    
    # Verify the result is a DataFrame
    assert isinstance(result, pd.DataFrame)
    
    # Verify the DataFrame has the expected columns
    expected_columns = [
        'article_id', 'title', 'description', 'content',
        'published_utc', 'ticker', 'sentiment_score',
        'keywords', 'source', 'ingestion_timestamp'
    ]
    assert all(col in result.columns for col in expected_columns)
    
    # Verify the data was transformed correctly
    assert result.iloc[0]['article_id'] == '123'
    assert result.iloc[0]['title'] == 'Test Article'
    assert result.iloc[0]['description'] == 'Test Description'
    assert result.iloc[0]['content'] == 'Test Content'
    assert result.iloc[0]['ticker'] == ['AAPL']
    assert result.iloc[0]['keywords'] == ['test', 'news']
    assert result.iloc[0]['source'] == 'Test Publisher' 