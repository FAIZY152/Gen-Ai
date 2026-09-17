from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    tenant_id: str = "demo-tenant"
    top_k: int = Field(default=5, ge=1, le=20)

class Source(BaseModel):
    document_id: str
    chunk_id: str
    source_name: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
