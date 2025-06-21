"""Simple investment analysis using collected data"""

import asyncio
from src.data_ingestion.financial_news import FinancialNewsIngestion
from src.vector_db.database import FinancialVectorDatabase
from src.models.llm import FinancialLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter

class InvestmentAnalyzer:
    def __init__(self):
        self.news_ingestion = FinancialNewsIngestion()
        self.vector_db = FinancialVectorDatabase()
        self.llm = FinancialLLM()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
    async def analyze_investment(self, ticker: str, question: str):
        # 1. Fetch news
        print(f"Fetching news for {ticker}...")
        news_articles = await self.news_ingestion.extract_real_time_news([ticker])
        
        if not news_articles:
            return f"No news found for {ticker}. Cannot perform analysis."

        # 2. Process and chunk documents
        all_chunks = []
        all_metadatas = []
        for article in news_articles:
            document = f"Title: {article['title']}\n\n{article['content']}"
            chunks = self.text_splitter.split_text(document)
            all_chunks.extend(chunks)
            
            # Create corresponding metadatas for each chunk
            for chunk in chunks:
                all_metadatas.append({
                    'source': article.get('source'),
                    'published_utc': article.get('published_utc'),
                    'article_url': article.get('article_url')
                })

        # 3. Add to vector database
        print(f"Adding {len(all_chunks)} news chunks to the vector database...")
        # Use the document itself as its ID for simple deduplication
        ids = [str(hash(chunk)) for chunk in all_chunks]
        self.vector_db.add_documents(documents=all_chunks, metadatas=all_metadatas, ids=ids)

        # 4. Query for relevant context
        print(f"Querying for documents relevant to: '{question}'")
        context_docs = self.vector_db.query(query_text=question, n_results=5)
        
        context_str = "\n\n---\n\n".join(context_docs['documents'][0])

        prompt = f"""
        User Question: {question}

        Context from financial news:
        ---
        {context_str}
        ---

        Based on the above context, please provide a financial analysis and recommendation.
        """

        print("\n--- PROMPT FOR LLM ---")
        print(prompt)
        print("--- END OF PROMPT ---\n")

        # 5. Generate analysis from the LLM
        print("Generating analysis from the financial LLM...")
        llm_response = self.llm.generate(prompt)
        
        return {
            "llm_response": llm_response,
            "retrieved_context": context_docs['documents'][0]
        }

# Example of how to run this
async def main():
    analyzer = InvestmentAnalyzer()
    ticker = "MSFT" # Using a different ticker for variety
    question = "What are the latest developments for Microsoft regarding AI?"
    result = await analyzer.analyze_investment(ticker, question)
    print("--- ANALYSIS RESULT ---")
    print(result)
    print("--- END OF RESULT ---")


if __name__ == "__main__":
    # This allows the script to be run directly to test the analyzer
    # You will need to have your POLYGON_API_KEY set in your environment
    asyncio.run(main())
