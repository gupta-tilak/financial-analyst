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
    
    # Verify the result is a list
    assert isinstance(result, list)
    
    # If we got results, verify the structure of the first article
    if result:
        first_article = result[0]
        # Verify the result contains expected keys
        assert 'article_id' in first_article
        assert 'title' in first_article
        assert 'description' in first_article
        assert 'content' in first_article
        assert 'published_utc' in first_article
        assert 'ticker' in first_article
        assert 'sentiment_score' in first_article
        assert 'keywords' in first_article
        assert 'source' in first_article
        assert 'author' in first_article
        assert 'article_url' in first_article
        assert 'image_url' in first_article
        assert 'ingestion_timestamp' in first_article

@pytest.mark.asyncio
async def test_extract_real_time_news_multiple_tickers(news_ingestion):
    # Test with multiple tickers
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    result = await news_ingestion.extract_real_time_news(tickers)
    
    # Verify the result is a list
    assert isinstance(result, list)
    
    # If we got results, verify the structure of the first article
    if result:
        first_article = result[0]
        # Verify the result contains expected keys
        assert 'article_id' in first_article
        assert 'title' in first_article
        assert 'description' in first_article
        assert 'content' in first_article
        assert 'published_utc' in first_article
        assert 'ticker' in first_article
        assert 'sentiment_score' in first_article
        assert 'keywords' in first_article
        assert 'source' in first_article
        assert 'author' in first_article
        assert 'article_url' in first_article
        assert 'image_url' in first_article
        assert 'ingestion_timestamp' in first_article

@pytest.mark.asyncio
async def test_transform_news_data(news_ingestion):
    # Sample raw data matching the new structure
    raw_data = [{
        'id': '123',
        'title': 'Test Article',
        'description': 'Test Description',
        'published_utc': datetime.now().isoformat(),
        'tickers': ['AAPL'],
        'keywords': ['test', 'news'],
        'publisher': {'name': 'Test Publisher'},
        'author': 'Test Author',
        'article_url': 'https://example.com/article',
        'image_url': 'https://example.com/image.jpg'
    }]
    
    # Transform the data
    result = news_ingestion.transform_news_data(raw_data)
    
    # Verify the result is a DataFrame
    assert isinstance(result, pd.DataFrame)
    
    # Verify the DataFrame has the expected columns
    expected_columns = [
        'article_id', 'title', 'description', 'content',
        'published_utc', 'ticker', 'sentiment_score',
        'keywords', 'source', 'author', 'article_url', 
        'image_url', 'ingestion_timestamp'
    ]
    assert all(col in result.columns for col in expected_columns)
    
    # Verify the data was transformed correctly
    assert result.iloc[0]['article_id'] == '123'
    assert result.iloc[0]['title'] == 'Test Article'
    assert result.iloc[0]['description'] == 'Test Description'
    assert result.iloc[0]['content'] == 'Test Description'  # content uses description
    assert result.iloc[0]['ticker'] == ['AAPL']
    assert result.iloc[0]['keywords'] == ['test', 'news']
    assert result.iloc[0]['source'] == 'Test Publisher'
    assert result.iloc[0]['author'] == 'Test Author'
    assert result.iloc[0]['article_url'] == 'https://example.com/article'
    assert result.iloc[0]['image_url'] == 'https://example.com/image.jpg' 