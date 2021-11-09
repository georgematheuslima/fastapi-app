from typing import List
from uuid import uuid4, UUID

from fastapi import FastAPI, HTTPException

from model import User, Gender, Role, UserUpdateRequest

app = FastAPI()

db: List[User] = [
    User(
        id=UUID("a6ba27cc-f112-413c-a71f-81674f2964ff"),
        first_name="George",
        last_name="Araújo",
        gender=Gender.male,
        roles=[Role.admin]
    ),
    User(
        id=UUID("d7e8d164-40f4-4933-a54a-c08a89941667"),
        first_name="Maria",
        last_name="do teste",
        gender=Gender.female,
        roles=[Role.student]
    )
]


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
    raise HTTPException(
        status_code=404,
        detail=f"User with id: {user_id} does not exists"
    )


@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
        raise HTTPException(
            status_code=404,
            detail=f"User with id: {user_id} dos not exists"
        )
