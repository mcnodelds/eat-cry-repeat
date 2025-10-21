from collections.abc import Sequence
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import select

from eatcryrepeat.db import FoodEntry, User, sessions
from eatcryrepeat.auth import Token
from eatcryrepeat.ai import RoastMode, roast, FoodDescription

router = APIRouter()


class FoodEntryIn(BaseModel):
    name: str
    media_base64: str | None = None
    notes: str | None = None
    roast_mode: str | None = "medium"


class FoodEntryOut(FoodEntryIn):
    id: int
    user_id: int
    calories: float
    protein_g: float | None
    fat_g: float | None
    carbs_g: float | None
    roast: str
    created_at: datetime


@router.post("/")
async def create_entry(token: str, body: FoodEntryIn) -> FoodEntryOut:
    email = Token(token=token).email()

    async with sessions() as db, db.begin():
        user = (
            await db.execute(select(User).where(User.email == email))
        ).scalar_one_or_none()
        if not user:
            raise HTTPException(401, "User not found")

        food_info = await roast(
            FoodDescription(
                name=body.name,
                media_base64=body.media_base64,
                notes=body.notes,
                roast_mode=RoastMode(body.roast_mode) or RoastMode.thatmom,
            ),
        )

        entry = FoodEntry(
            user_id=user.id,
            name=body.name,
            calories=food_info.calories,
            protein_g=food_info.protein_g,
            fat_g=food_info.fat_g,
            carbs_g=food_info.carbs_g,
            media_base64=body.media_base64,
            notes=body.notes,
        )
        db.add(entry)
        await db.flush()
        await db.refresh(entry)

        return FoodEntryOut(
            id=entry.id,
            user_id=entry.user_id,
            name=entry.name,
            calories=entry.calories,
            protein_g=entry.protein_g,
            fat_g=entry.fat_g,
            carbs_g=entry.carbs_g,
            media_base64=entry.media_base64,
            notes=entry.notes,
            roast=food_info.roast,
            created_at=entry.created_at,
        )


@router.get("/")
async def list_entries(token: str) -> Sequence[FoodEntryOut]:
    email = Token(token=token).email()

    async with sessions() as db, db.begin():
        user = (
            await db.execute(select(User).where(User.email == email))
        ).scalar_one()

        rows = (
            (
                await db.execute(
                    select(FoodEntry)
                    .where(FoodEntry.user_id == user.id)
                    .order_by(FoodEntry.created_at.desc())
                )
            )
            .scalars()
            .all()
        )

        return [
            FoodEntryOut(
                id=r.id,
                user_id=r.user_id,
                name=r.name,
                calories=r.calories,
                protein_g=r.protein_g,
                fat_g=r.fat_g,
                carbs_g=r.carbs_g,
                media_base64=r.media_base64,
                notes=r.notes,
                roast=r.notes or "",
                created_at=r.created_at,
            )
            for r in rows
        ]
