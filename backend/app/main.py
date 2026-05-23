from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

from fastapi import UploadFile, File
from .ingest_file import ingest_text_file

from .ingest import ingest_confluence
from .vectorstore import load_vectorstore
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

app = FastAPI()

class IngestRequest(BaseModel):
    space_key: str = None
    limit: int = 500

class ChatRequest(BaseModel):
    query: str
    k: int = 4

@app.post("/ingest-file")
async def ingest_file(file: UploadFile = File(...)):
    """
    Upload a text file and index its content
    """
    try:
        # Save temporary file
        tmp_path = f"/tmp/{file.filename}"
        with open(tmp_path, "wb") as f:
            f.write(await file.read())
        result = ingest_text_file(tmp_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
def ingest(req: IngestRequest):
    try:
        res = ingest_confluence(space_key=req.space_key, limit=req.limit)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        vs = load_vectorstore()
        retriever = vs.as_retriever(search_kwargs={"k": req.k})
        llm = ChatOpenAI(temperature=0, model=os.getenv("LLM_MODEL", "gpt-4o-mini"))

        template = """You are a helpful assistant. Use the following extracted Confluence page content to answer the question.
        If the answer is not contained in the context, say "I don't know." Provide a short answer and then list sources (title and url).

        =========
        {context}
        =========
        Question: {question}
        Answer:"""
        prompt = PromptTemplate(template=template, input_variables=["context", "question"])

        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
        result = qa({"query": req.query})
        answer_text = result.get("result")
        docs = result.get("source_documents", [])
        sources = [{"title": d.metadata.get("title"), "url": d.metadata.get("source")} for d in docs]
        return {"answer": answer_text, "sources": sources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))