from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    name: str = Field(min_length=1, max_length=120)
    # admin через публичный API недостижим — назначается только вручную в БД
    role: str = Field(default="author", pattern="^(author|designer|client)$")


class UserRead(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: EmailStr
    password: str