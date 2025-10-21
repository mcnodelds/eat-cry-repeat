from collections.abc import Mapping
from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def hello() -> Mapping[str, Any]:
    return {"hello": "world"}


