import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Model settings
BASE_MODEL = "meta-llama/Llama-2-7b-hf"  # or any open model
FINE_TUNED_MODEL_PATH = BASE_DIR / "data" / "models" / "financial_model"

# Data paths
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# API Keys (from environment)
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Vector Database
VECTOR_DB_PATH = DATA_DIR / "vector_db"

# Training settings
LORA_R = 16
LORA_ALPHA = 16
LEARNING_RATE = 2e-4
BATCH_SIZE = 4
MAX_LENGTH = 512

# Sample tickers for demo
DEMO_TICKERS = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"]
