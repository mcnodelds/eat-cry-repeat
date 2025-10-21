import base64
from enum import StrEnum
import enum

from google.genai import Client
from google.genai.types import GenerateContentConfig, Part

from pydantic import BaseModel

from eatcryrepeat.config import settings


client = Client(api_key=settings.GOOGLE_AI_API_KEY)


class RoastMode(StrEnum):
    glutenfree = enum.auto()
    thatmom = enum.auto()
    ode_to_obesity = enum.auto()

    def prompt(self) -> str:
        if self == RoastMode.glutenfree:
            return ...

        if self == RoastMode.thatmom:
            return ...

        if self == RoastMode.ode_to_obesity:
            return ...

        return "єбу блять"


class FoodDescription(BaseModel):
    name: str
    media_base64: str | None = None
    notes: str | None = None
    roast_mode: RoastMode = RoastMode.thatmom


class FoodInfo(BaseModel):
    calories: float
    protein_g: float | None
    fat_g: float | None
    carbs_g: float | None
    roast: str = ""


async def roast(description: FoodDescription) -> FoodInfo:
    result = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            description.notes or "",
            *(
                [
                    Part.from_bytes(
                        data=base64.b64decode(description.media_base64 or ""),
                        mime_type="image/png",
                    )
                ]
                if description.media_base64
                else ()
            ),
        ],
        config=GenerateContentConfig(
            response_schema=FoodInfo,
            system_instruction=description.roast_mode.prompt(),
            response_mime_type="application/json",
        ),
    )

    return FoodInfo.model_validate(result.parsed)
