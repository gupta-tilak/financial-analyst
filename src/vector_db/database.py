# Vector Database Configuration
from sentence_transformers import SentenceTransformer
import numpy as np
import chromadb

class FinancialVectorDatabase:
    def __init__(self, collection_name="financial_news"):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"} # Using cosine similarity
        )

    def add_documents(self, documents, metadatas=None, ids=None):
        """
        Adds documents to the collection.

        Args:
            documents (list of str): The documents to add.
            metadatas (list of dict, optional): Metadata for each document.
            ids (list of str, optional): Unique IDs for each document.
        """
        if not documents:
            return

        embeddings = self.embedding_model.encode(documents, convert_to_tensor=False).tolist()
        
        # ChromaDB requires string IDs. If not provided, create them.
        if ids is None:
            # simple hashing for id generation
            ids = [str(hash(doc)) for doc in documents]

        self.collection.upsert(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_text, n_results=5):
        """
        Queries the collection for similar documents.

        Args:
            query_text (str): The text to search for.
            n_results (int): The number of results to return.

        Returns:
            dict: The query results.
        """
        query_embedding = self.embedding_model.encode(query_text, convert_to_tensor=False).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results

    def get_collection_count(self):
        """Returns the number of items in the collection."""
        return self.collection.count()
