from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/user",
    tags=["User"]
)




@router.get("/")
def get_users():
    return {
        "users": []
    }