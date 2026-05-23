from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from .confluence_client import fetch_pages_from_space
from .vectorstore import create_vectorstore_from_documents

def ingest_confluence(space_key: str = None, limit: int = 500):
    pages = fetch_pages_from_space(space_key=space_key, limit=limit)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = []
    for p in pages:
        text = p["body"] or ""
        if not text.strip():
            continue
        chunks = splitter.split_text(text)
        for i, c in enumerate(chunks):
            metadata = {
                "source": p["url"],
                "title": p["title"],
                "page_id": p["id"],
                "chunk": i
            }
            docs.append(Document(page_content=c, metadata=metadata))
    vs = create_vectorstore_from_documents(docs)
    return {"ingested_pages": len(pages), "ingested_chunks": len(docs)}
