import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

class PolicyEngine:
    def __init__(self, index_path="data/processed/faiss_index"):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        if os.path.exists(index_path):
            self.vector_store = FAISS.load_local(
                index_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            raise FileNotFoundError(f"Index not found at {index_path}. Run ingestion first!")

    
    def search(self, query, k=3):
        
        docs = self.vector_store.similarity_search(query, k=k)
        return docs
