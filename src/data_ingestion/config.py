"""
Configuration file for API keys and other settings
"""

# API Keys
POLYGON_API_KEY = "jFQ9xrxHDKY8rXdpPT9dAWd1P69NZ4XU"
ALPHA_VANTAGE_API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"
NEWSAPI_API_KEY = "YOUR_NEWSAPI_API_KEY"

# API Endpoints
API_ENDPOINTS = {
    'polygon': 'https://api.polygon.io/v2/reference/news',
    'alpha_vantage': 'https://www.alphavantage.co/query',
    'newsapi': 'https://newsapi.org/v2/everything',
    'reuters': 'https://reuters.com/finance',
    'bloomberg': 'https://bloomberg.com/markets'
}

# Rate Limiting Configuration
POLYGON_RATE_LIMIT = {
    'requests_per_minute': 5,  # Conservative limit to avoid 429 errors
    'max_retries': 3,
    'base_delay': 30,  # Base delay for exponential backoff (seconds)
    'enable_jitter': True  # Add random jitter to avoid thundering herd
} 