from pydantic import BaseSettings,BaseModel

class Settings(BaseSettings):
    groq_api_key: str
    groq_model_id: str

    database_url: str

    max_retries: int = 3
    request_timeout: int = 10

   

settings = Settings()