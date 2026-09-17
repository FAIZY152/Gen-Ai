from uuid import uuid4
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from app.core.config import settings
from app.services.embedding_service import embed_query, embed_texts

class RetrievalService:
    def __init__(self):
        self.client = QdrantClient(url=settings.QDRANT_URL)
        self.collection = settings.QDRANT_COLLECTION
        self._ensure_collection()

    def _ensure_collection(self):
        dimension = len(embed_query("dimension probe"))
        names = [item.name for item in self.client.get_collections().collections]
        if self.collection not in names:
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=dimension, distance=Distance.COSINE),
            )

    def upsert_chunks(self, chunks: list[str], metadata: dict) -> int:
        vectors = embed_texts(chunks)
        points = []
        for index, (chunk, vector) in enumerate(zip(chunks, vectors)):
            payload = {
                **metadata,
                "chunk_id": f"{metadata['document_id']}-{index}",
                "text": chunk,
            }
            points.append(PointStruct(id=str(uuid4()), vector=vector, payload=payload))
        self.client.upsert(collection_name=self.collection, points=points)
        return len(points)

    def search(self, query: str, tenant_id: str, top_k: int):
        query_filter = Filter(must=[
            FieldCondition(key="tenant_id", match=MatchValue(value=tenant_id))
        ])
        return self.client.search(
            collection_name=self.collection,
            query_vector=embed_query(query),
            query_filter=query_filter,
            limit=top_k,
        )

retrieval_service = RetrievalService()
