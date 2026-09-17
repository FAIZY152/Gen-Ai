from pydantic import BaseModel, Field

class IngestTextRequest(BaseModel):
    text: str = Field(min_length=1)
    document_id: str
    tenant_id: str = "demo-tenant"
    source_name: str = "manual-input"

class IngestResponse(BaseModel):
    document_id: str
    chunks_created: int
    status: str
