#!/usr/bin/env python3
"""
Financial Market Analyst
Main entry point for the application
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.data_ingestion.news_scraper import NewsCollector
from src.data_ingestion.sec_filings import SECCollector
from src.models.lora_trainer import FinancialModelTrainer
from src.analysis.investment_analyzer import InvestmentAnalyzer
from src.api.app import create_app

def main():
    parser = argparse.ArgumentParser(description="Financial Market Analyst")
    parser.add_argument("--mode", choices=["collect", "train", "analyze", "api"], 
                       required=True, help="Operation mode")
    parser.add_argument("--ticker", type=str, help="Stock ticker to analyze")
    
    args = parser.parse_args()
    
    if args.mode == "collect":
        print("📊 Collecting financial data...")
        collector = NewsCollector()
        collector.collect_recent_news()
        
        sec_collector = SECCollector()
        sec_collector.collect_filings(["AAPL", "GOOGL", "MSFT"])
        
    elif args.mode == "train":
        print("🤖 Training financial model...")
        trainer = FinancialModelTrainer()
        trainer.train_model()
        
    elif args.mode == "analyze":
        if not args.ticker:
            print("❌ Please provide a ticker with --ticker")
            return
            
        print(f"💡 Analyzing {args.ticker}...")
        analyzer = InvestmentAnalyzer()
        result = analyzer.analyze_stock(args.ticker)
        print(f"Investment Recommendation: {result}")
        
    elif args.mode == "api":
        print("🚀 Starting API server...")
        app = create_app()
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
