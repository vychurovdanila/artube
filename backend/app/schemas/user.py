from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    name: str = Field(min_length=1, max_length=120)
    # Поле role УДАЛЕНО — при регистрации всегда ставим ["client"]


class UserRead(BaseModel):
    id: int
    email: Optional[EmailStr] = None
    name: str
    roles: List[str]  # Массив ролей
    telegram_username: Optional[str] = None
    avatar_url: Optional[str] = None

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: EmailStr
    password: str
