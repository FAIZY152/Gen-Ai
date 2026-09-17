from app.schemas.chat_schema import ChatRequest
from app.services.retrieval_service import retrieval_service
from app.services.generation_service import generation_service

class RagService:
    def answer(self, payload: ChatRequest):
        results = retrieval_service.search(payload.question, payload.tenant_id, payload.top_k)
        context_parts = []
        sources = []

        for result in results:
            data = result.payload or {}
            context_parts.append(
                f"Source: {data.get('source_name', 'unknown')}\n"
                f"Content: {data.get('text', '')}"
            )
            sources.append({
                "document_id": data.get("document_id", ""),
                "chunk_id": data.get("chunk_id", ""),
                "source_name": data.get("source_name", "unknown"),
            })

        answer = generation_service.generate(
            payload.question,
            "\n\n---\n\n".join(context_parts),
        )
        return {"answer": answer, "sources": sources}

rag_service = RagService()
