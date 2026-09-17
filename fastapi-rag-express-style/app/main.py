from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.routes import api_router

app = FastAPI(title="FastAPI RAG API", version="1.0.0")
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.ENVIRONMENT}
