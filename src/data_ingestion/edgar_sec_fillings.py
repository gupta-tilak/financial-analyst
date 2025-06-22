# EDGAR SEC Filings Pipeline
import requests
import xml.etree.ElementTree as ET
from sec_edgar_downloader import Downloader
from typing import List, Dict
import schedule
import time
import os

class EDGARDataIngestion:
    def __init__(self):
        self.base_url = "https://www.sec.gov/Archives/edgar/data"
        self.filing_types = ['10-K', '10-Q', '8-K', '13F', 'DEF 14A']
        self.headers = {'User-Agent': 'YourCompany yourname@company.com'}
        
    def batch_extract_filings(self, cik_list: List[str], filing_type: str):
        """Batch processing for SEC filings as recommended"""
        downloader = Downloader("YourCompany", "yourname@company.com")
        
        filings_data = []
        
        for cik in cik_list:
            try:
                # Download filings for past quarter
                filings = downloader.get(filing_type, cik, 
                                       after="2024-01-01", 
                                       before="2024-12-31")
                
                for filing in filings:
                    parsed_data = self.parse_filing_content(filing)
                    filings_data.append(parsed_data)
                    
            except Exception as e:
                print(f"Error processing CIK {cik}: {e}")
                
        return filings_data
    
    def parse_filing_content(self, filing_path: str) -> Dict:
        """Extract key financial metrics from XBRL data"""
        # Parse XBRL financial data
        try:
            tree = ET.parse(filing_path)
            root = tree.getroot()
            
            financial_data = {
                'filing_date': self.extract_filing_date(root),
                'total_revenue': self.extract_metric(root, 'us-gaap:Revenues'),
                'net_income': self.extract_metric(root, 'us-gaap:NetIncomeLoss'),
                'total_assets': self.extract_metric(root, 'us-gaap:Assets'),
                'total_liabilities': self.extract_metric(root, 'us-gaap:Liabilities'),
                'stockholders_equity': self.extract_metric(root, 'us-gaap:StockholdersEquity'),
                'operating_cash_flow': self.extract_metric(root, 'us-gaap:NetCashProvidedByUsedInOperatingActivities'),
                'risk_factors': self.extract_risk_factors(root),
                'management_discussion': self.extract_mda(root)
            }
            
            return financial_data
            
        except Exception as e:
            return {'error': f"Parsing failed: {e}"}
    
    def schedule_daily_updates(self):
        """Schedule batch processing during off-peak hours"""
        # EDGAR filing deadlines vary by form type as mentioned in search results
        schedule.every().day.at("02:00").do(self.batch_extract_filings)
        schedule.every().day.at("18:00").do(self.extract_recent_8k_filings)
