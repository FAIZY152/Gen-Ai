from fastapi import APIRouter
from app.api.v1.document_router import router as document_router
from app.api.v1.chat_router import router as chat_router

api_router = APIRouter()
api_router.include_router(document_router, prefix="/documents", tags=["Documents"])
api_router.include_router(chat_router, prefix="/chat", tags=["Chat"])
