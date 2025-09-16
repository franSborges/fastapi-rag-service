from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Tuple
import re 
from collections import Counter

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

def calculate_chunk_relevance(chunk: str, question_words: List[str], doc_title: str) -> Dict:
    
 chunk_lower = chunk.lower() 
 title_lower = doc_title.lower()  
 
 words_found = []
 for word in question_words:
     word_clean = re.sub(r'[^\w]', '', word.lower())
     if len(word_clean) > 2:
         if word_clean in chunk_lower:
             words_found.append(word_clean)
             
 word_math_score = len(words_found)
 word_density = len(words_found) / len(question_words) if question_words else 0
 
  
 title_bonus = 0
 for word in words_found:
     if word in title_lower:
         title_bonus += 0.5
         
         
 length_penalty = 0 if len(chunk.strip()) > 10 else -1
 
 final_score = word_math_score + word_density + title_bonus + length_penalty
 
 return {
     'chunk': chunk,
     'doc_title': doc_title,
     'score': final_score,
     'words_found': words_found,
     'word_count': word_math_score,
     'density': word_density
 }
  



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