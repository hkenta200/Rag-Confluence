import os
from typing import List
from langchain.schema import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import PGVector

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "rag_db")
EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

def get_pgvector_url():
    return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

def create_vectorstore_from_documents(docs: List[Document], persist=True):
    emb = OpenAIEmbeddings(model=EMBED_MODEL)
    vs = PGVector.from_documents(
        documents=docs,
        embedding=emb,
        collection_name="confluence_docs",
        connection_string=get_pgvector_url()
    )
    return vs

def load_vectorstore():
    emb = OpenAIEmbeddings(model=EMBED_MODEL)
    return PGVector(
        collection_name="confluence_docs",
        embedding_function=emb.embed_query,
        connection_string=get_pgvector_url()
    )
