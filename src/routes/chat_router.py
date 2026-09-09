from fastapi import APIRouter, Body
from ..controller.chat_service import ChatService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


chat_service = ChatService()

@router.get("/health")
def health():
    return {"status": "chat service is running"}



@router.post("/message")
async def get_message(userinpt: str = Body(..., embed=True)):
    response = chat_service.generate_response(userinpt)
    return {"response": response}
