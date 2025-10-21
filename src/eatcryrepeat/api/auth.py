from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import select

from eatcryrepeat.db import User, sessions
from eatcryrepeat.auth import Token, pwd


router = APIRouter()


class Register(BaseModel):
    email: EmailStr
    username: str
    password: str


@router.post("/register")
async def register(body: Register) -> Token:
    async with sessions() as db, db.begin():
        user = (
            await db.execute(select(User).where(User.email == body.email))
        ).scalar_one_or_none()

        if user is not None:
            raise HTTPException(400, "Email already used")

        db.add(
            User(
                email=body.email,
                username=body.username,
                hashed_password=pwd.hash(body.password),
            )
        )

        return Token.from_sub(body.email)


class Login(BaseModel):
    email: EmailStr
    password: str


@router.post("/login")
async def login(body: Login) -> Token:
    async with sessions() as db, db.begin():
        user = (
            await db.execute(select(User).where(User.email == body.email))
        ).scalar_one_or_none()

        if not user or not pwd.verify(body.password, user.hashed_password):
            raise HTTPException(401, "Invalid email or password")

    return Token.from_sub(user.email)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    age: int | None
    gender: str | None
    weight_kg: float | None
    height_cm: float | None
    activity_level: str | None


@router.get("/me")
async def me(token: str) -> UserResponse:
    email = Token(token=token).email()
    async with sessions() as db, db.begin():
        user = (
            await db.execute(select(User).where(User.email == email))
        ).scalar_one()

        return UserResponse.model_validate(user, from_attributes=True)
