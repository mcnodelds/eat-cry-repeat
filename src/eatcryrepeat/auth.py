from datetime import UTC, datetime, timedelta
from typing import Self, final
from jose import jwt
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

from eatcryrepeat.config import settings

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


@final
class Token(BaseModel):
    token: str

    @classmethod
    def from_sub(cls, sub: str) -> Self:
        exp = datetime.now(tz=UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        return cls(
            token=jwt.encode(
                {"sub": sub, "exp": exp},
                settings.SECRET_KEY,
                settings.ALGORITHM,
            )
        )

    def email(self) -> EmailStr:
        claims = jwt.decode(
            self.token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        return claims.get("sub", "")
