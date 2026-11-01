from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TelegramAuthPayload(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None
    auth_date: int
    hash: str

    model_config = {"extra": "allow"}  # Telegram может прислать доп. поля, они участвуют в HMAC