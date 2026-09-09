from fastapi import FastAPI
from src.routes.chat_router import router as chat_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="AI Backend",
    version="1.0.0",
)

app.include_router(
    chat_router,
    prefix="/api",
    tags=["AI"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}
