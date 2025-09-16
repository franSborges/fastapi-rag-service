from fastapi import FastAPI
from api.v1 import router as v1_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI RAG Service",
        description="RAG service with local testing",
        version="0.1.0"
    )
    app.include_router(v1_router)
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)