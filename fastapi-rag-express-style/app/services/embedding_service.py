from functools import lru_cache
from sentence_transformers import SentenceTransformer
from app.core.config import settings

@lru_cache
def get_model():
    return SentenceTransformer(settings.EMBEDDING_MODEL)

def embed_texts(texts: list[str]) -> list[list[float]]:
    vectors = get_model().encode(texts, normalize_embeddings=True)
    return vectors.tolist()

def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]
