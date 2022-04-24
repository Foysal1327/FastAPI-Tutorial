from http.client import HTTPException
from fastapi import FastAPI, HTTPException
from typing import List
from models import Role, User, Gender, UserUpdate
from uuid import UUID, uuid4

app = FastAPI()

db: List[User] = [
    User(id = "a0f37d58-e24c-46ed-902d-67f5177a3063",
    first_name = "Karim",
    last_name = "Rahman",
    gender = Gender.male,
    role = [Role.student]
    ),
    User(id = "674250a2-99e2-4f62-9821-7e7e30f09054",
    first_name = "Jasmin",
    last_name = "Rahman",
    gender = Gender.female,
    role = [Role.admin, Role.user]
    )
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/users")
async def get_users():
    return db

@app.post("/api/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return "user has been deleted"
    raise HTTPException(
        status_code=404,
        detail=f"user with {user_id} id not found."
    )

@app.put("/api/users/{user_id}")
async def update_user(user_update: User, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.gender is not None:
                user.gender = user_update.gender
            if user_update.role is not None:
                user.role = user_update.role
            return "user has been updated"
    raise HTTPException(
        status_code=404,
        detail=f"user with {user_id} id not found."
    )

