from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
    verify_telegram_signature,
)
from app.models.user import User
from app.schemas.auth import TelegramAuthPayload, Token
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        name=payload.name,
        roles=["client"],
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if user and not user.password_hash:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="This account uses Telegram login",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(subject=user.email, role=", ".join(user.roles))
    return Token(access_token=token)


@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/telegram", response_model=Token)
def telegram_login(payload: TelegramAuthPayload, db: Session = Depends(get_db)):
    data = payload.model_dump(exclude_none=True)

    if not verify_telegram_signature(data, settings.TELEGRAM_BOT_TOKEN):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Telegram signature",
        )

    user = db.query(User).filter(User.telegram_id == payload.id).first()

    if user is None:
        user = User(
            email=None,
            password_hash=None,
            roles=["client"],
            name=payload.first_name or payload.username or f"tg_{payload.id}",
            telegram_id=payload.id,
            telegram_username=payload.username,
            avatar_url=payload.photo_url,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # Обновляем актуальные данные из Telegram
        user.telegram_username = payload.username
        user.avatar_url = payload.photo_url
        db.commit()
        db.refresh(user)

    subject = user.email or f"tg:{user.telegram_id}"
    token = create_access_token(subject=subject, role=", ".join(user.roles))
    return Token(access_token=token)
