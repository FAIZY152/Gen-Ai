# create dummy db
from fastapi import HTTPException

users = [
    {
        "id": 1,
        "name": "khan",
        "age": 20,
        "city":"Peshawar"
    },
    {
            "id": 2,
            "name": "Muhammad",
            "age": 23,
            "city":"Lahore"
        },
]


def get_users():
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return users


def get_user_by_id(id: int):
    for user in users:
        if user["id"] == id:
            return user
        raise HTTPException(status_code=404, detail="User not found")

def create_user(payload: dict):

    # if user name is exist dont add it
    for user in users:
        if user["name"] == payload["name"]:
            raise HTTPException(status_code=400, detail="User already exist")
        else:
          users.append(payload)
    return payload


def update_user(id: int, payload: dict):
    for i, user in enumerate(users):
        if user["id"] == id:
            users[i] = payload
            return payload
        raise HTTPException(status_code=404, detail="User not found")
    

def delete_user(id: int):
    for i, user in enumerate(users):
        if user["id"] == id:
            del users[i]
            return {"message": "User deleted successfully"}
        raise HTTPException(status_code=404, detail="User not found")






