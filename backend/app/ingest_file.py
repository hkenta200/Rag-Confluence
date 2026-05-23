from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from .vectorstore import create_vectorstore_from_documents
from typing import List

def ingest_text_file(file_path: str):
    """
    Reads a text file, splits it into chunks, and indexes into PGVector
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        raise ValueError(f"Failed to read file {file_path}: {e}")

    if not text.strip():
        return {"ingested_chunks": 0, "message": "Empty file"}

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_text(text)

    docs = []
    for i, c in enumerate(chunks):
        metadata = {
            "source": file_path,
            "title": f"File: {file_path}",
            "chunk": i
        }
        docs.append(Document(page_content=c, metadata=metadata))

    vs = create_vectorstore_from_documents(docs)
    return {"ingested_chunks": len(docs), "source": file_path}
