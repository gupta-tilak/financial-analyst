# Vector Database Configuration
import weaviate
import openai
from sentence_transformers import SentenceTransformer
import numpy as np

class FinancialVectorDatabase:
    def __init__(self):
        # Initialize Weaviate client as recommended for financial applications
        self.client = weaviate.Client(
            url="http://localhost:8080",
            additional_headers={
                "X-OpenAI-Api-Key": "your-openai-key"
            }
        )
        
        # Financial-specific embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.setup_financial_schema()
    
    def setup_financial_schema(self):
        """Create schema optimized for financial documents"""
        # Financial News Schema
        news_schema = {
            "class": "FinancialNews",
            "description": "Financial news articles with market insights",
            "vectorizer": "text2vec-openai",
            "properties": [
                {"name": "title", "dataType": ["text"]},
                {"name": "content", "dataType": ["text"]},
                {"name": "ticker", "dataType": ["string[]"]},
                {"name": "publishedDate", "dataType": ["date"]},
                {"name": "sentimentScore", "dataType": ["number"]},
                {"name": "source", "dataType": ["string"]},
                {"name": "keywords", "dataType": ["string[]"]},
                {"name": "marketImpact", "dataType": ["string"]}
            ]
        }
        
        # SEC Filings Schema
        sec_schema = {
            "class": "SECFiling",
            "description": "SEC filings and financial statements",
            "vectorizer": "text2vec-openai",
            "properties": [
                {"name": "cik", "dataType": ["string"]},
                {"name": "ticker", "dataType": ["string"]},
                {"name": "filingType", "dataType": ["string"]},
                {"name": "filingDate", "dataType": ["date"]},
                {"name": "period", "dataType": ["string"]},
                {"name": "financialMetrics", "dataType": ["object"]},
                {"name": "riskFactors", "dataType": ["text"]},
                {"name": "managementDiscussion", "dataType": ["text"]},
                {"name": "keyRatios", "dataType": ["object"]}
            ]
        }
        
        # Company Reports Schema
        reports_schema = {
            "class": "CompanyReport",
            "description": "Earnings calls and company presentations",
            "vectorizer": "text2vec-openai",
            "properties": [
                {"name": "ticker", "dataType": ["string"]},
                {"name": "reportType", "dataType": ["string"]},
                {"name": "quarter", "dataType": ["string"]},
                {"name": "transcript", "dataType": ["text"]},
                {"name": "keyMetrics", "dataType": ["object"]},
                {"name": "guidance", "dataType": ["text"]},
                {"name": "analystQuestions", "dataType": ["text"]},
                {"name": "managementTone", "dataType": ["string"]}
            ]
        }
        
        # Create schemas
        for schema in [news_schema, sec_schema, reports_schema]:
            self.client.schema.create_class(schema)
