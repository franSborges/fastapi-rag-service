from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

@router.get("/health")
def health():
    return {"status": "ok", "message": "FastAPI is running locally!"}

@router.get("/test")
def test():
    return {"message": "This is a test endpoint", "free_mode": True}