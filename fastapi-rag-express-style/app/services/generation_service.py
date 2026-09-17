from groq import Groq
from app.core.config import settings

class GenerationService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    def generate(self, question: str, context: str) -> str:
        system_prompt = (
            "You are a grounded knowledge assistant. Use only the supplied context. "
            "If the answer is missing, say you could not find it. Do not invent facts."
        )
        response = self.client.chat.completions.create(
            model=settings.GROQ_MODEL,
            temperature=0.1,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"},
            ],
        )
        return response.choices[0].message.content.strip()

generation_service = GenerationService()
