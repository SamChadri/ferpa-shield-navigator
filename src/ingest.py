import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

def run_ingestion():

    raw_data_path = "data/raw/"
    index_dest_path = "data/processed/faiss_index"

    documents = []
    pdf_files = [f for f in os.listdir(raw_data_path) if f.endswith(".pdf")]

    if not pdf_files:
        print("❌ No PDFs found in data/raw/. Drop a UIUC policy file there!")
        return

    for file in pdf_files:
        print(f"Loading {file}...")
        loader = PyPDFLoader(os.path.join(raw_data_path, file))
        documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", " "]
    )

    chunks = text_splitter.split_documents(documents)
    print(f"✂️ Split into {len(chunks)} chunks.")

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(chunks, embeddings)

    vector_store.save_local(index_dest_path)
    print(f"✅ Success! Vector index saved to {index_dest_path}")

if __name__ == "__main__":
    run_ingestion()