import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from dotenv import load_dotenv
from langchain_groq import ChatGroq

class PolicyEngine:
    def __init__(self, index_path="data/processed/faiss_index"):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        self.llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            temperature=0.2, # Lower temperature for factual accuracy
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        if os.path.exists(index_path):
            self.vector_store = FAISS.load_local(
                index_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            
        else:
            raise FileNotFoundError(f"Index not found at {index_path}. Run ingestion first!")

    def get_chat_chain(self, llm):
        return ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=self.vector_store.as_retriever(),
            memory=self.memory,
            return_source_documents=True
        )
    def get_chat_response(self, user_query, chat_history):
        chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True
        )
        
        result = chain.invoke({
            "question": user_query, 
            "chat_history": chat_history
        })
        
        return result["answer"], result["source_documents"]
    def search(self, query, k=3):
        
        docs = self.vector_store.similarity_search(query, k=k)
        return docs
