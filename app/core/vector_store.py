import os
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

CHROMA_DIR = "vector_db"
COLLECTION_NAME = "meeting_transcript"

def get_embeddings():
    return OllamaEmbeddings(
        model_name = EMBEDDING_MODEL,
        model_kwargs = {"device": 'cpu'}
    )

def build_vector_store(transcript: str) -> Chroma:
    print("Building vector store...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(transcript)
    docs = [
        Document(page_content=chunk)
        for chunk in chunks
    ]

    embeddings = get_embeddings()
    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name = COLLECTION_NAME,
        persist_directory=CHROMA_DIR
    )

    return vector_store

def load_vector()->Chroma:
    embeddings = get_embeddings()
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR
    )
    return vector_store

def get_retriver(vector_store: Chroma,k: int = 4):
    return vector_store.as_retriever(
        search_type = "similarity",
        search_kwargs = {"k":k}
    )