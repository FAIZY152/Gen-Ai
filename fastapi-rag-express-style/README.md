# FastAPI RAG — Express.js Style

## Run
```bash
cp .env.example .env
docker compose up -d qdrant
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs.

## Endpoints
- POST `/api/v1/documents/ingest`
- POST `/api/v1/chat`

This starter keeps document records in Qdrant payloads. Add PostgreSQL repositories, authentication, background workers, and migrations before calling it production-ready.
