# main.py
from fastapi import FastAPI
from .routes.UserRoute import router as user_router


# Create FastAPI application
app = FastAPI()


# Register agent routes
app.include_router(user_router)


# Health check
@app.get("/")
def home():

    return {
        "message": "API is running"
    }