from app.schemas.document_schema import IngestTextRequest
from app.services.chunking_service import split_text
from app.services.retrieval_service import retrieval_service

class IngestionService:
    def ingest_text(self, payload: IngestTextRequest):
        chunks = split_text(payload.text)
        count = retrieval_service.upsert_chunks(
            chunks,
            {
                "document_id": payload.document_id,
                "tenant_id": payload.tenant_id,
                "source_name": payload.source_name,
            },
        )
        return {
            "document_id": payload.document_id,
            "chunks_created": count,
            "status": "completed",
        }

ingestion_service = IngestionService()
