from fastapi import APIRouter

from eatcryrepeat.api.auth import router as auth_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth")
