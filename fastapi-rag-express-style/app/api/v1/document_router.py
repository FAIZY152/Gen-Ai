from fastapi import APIRouter
from app.schemas.document_schema import IngestTextRequest, IngestResponse
from app.services.ingestion_service import ingestion_service

router = APIRouter()

@router.post("/ingest", response_model=IngestResponse)
def ingest_document(payload: IngestTextRequest):
    return ingestion_service.ingest_text(payload)
