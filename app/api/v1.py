from fastapi import APIRouter
from typing import List 
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1")

class IngestRequest(BaseModel):
    text: str
    title: str = "untitled"

class QARequest(BaseModel):
    question: str

class QAResponse(BaseModel):
    answer: str
    sources: List[str]
    mock_mode: bool = True

mock_documents = []

@router.get("/health")
def health():
    return {"status": "ok", "message": "FastAPI is running locally!"}

@router.get("/test")
def test():
    return {"message": "This is a test endpoint", "free_mode": True}

@router.post("/ingest")
def ingest_document(request: IngestRequest):
    doc_id = len(mock_documents)
    mock_documents.append({
        "id": doc_id,
        "title": request.title,
        "text": request.text,
        "chunks": request.text.split(". ")
    })
    return {"message": f"Document '{request.title}' ingested", "doc_id": doc_id}

@router.post("/qa")
def ask_question(request: QARequest) -> QAResponse:
    relevant_chunks = []
    for doc in mock_documents:
        for chunk in doc["chunks"]:
            if any(word.lower() in chunk.lower() for word in request.question.split()):
                relevant_chunks.append(f"{doc['title']}: {chunk}")
    
    
    if relevant_chunks:
        answer = f"Based on the documents, here's what I found about '{request.question}': {relevant_chunks[0]}"
        sources = [chunk.split(":")[0] for chunk in relevant_chunks[:3]]
    else:
        answer = f"I couldn't find specific information about '{request.question}' in the uploaded documents."
        sources = []
    
    return QAResponse(answer=answer, sources=sources, mock_mode=True)

@router.get("/documents") 
def list_documents():
    return {"documents": [{"id": i, "title": doc["title"]} for i, doc in enumerate(mock_documents)]}