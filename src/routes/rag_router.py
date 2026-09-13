from fastapi import APIRouter

from app.services.rag_service import RAGService


router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)


rag_service = RAGService()


@router.post("/ingest")
async def ingest_document():

    return rag_service.ingest_document()


@router.get("/query")
async def query_rag(
    question: str
):

    return rag_service.generate_response(
        question
    )