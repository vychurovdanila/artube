from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database import SessionLocal
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def _find_user_by_subject(db: Session, sub: str) -> Optional[User]:
    if sub.startswith("tg:"):
        try:
            tg_id = int(sub[3:])
        except ValueError:
            return None
        return db.query(User).filter(User.telegram_id == tg_id).first()
    return db.query(User).filter(User.email == sub).first()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exc = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None or "sub" not in payload:
        raise credentials_exc
    user = _find_user_by_subject(db, payload["sub"])
    if user is None:
        raise credentials_exc
    return user


def require_role(*roles: str):
    def checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role required: {' or '.join(roles)}",
            )
        return current_user
    return checker


def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme_optional),
    db: Session = Depends(get_db),
) -> Optional[User]:
    if token is None:
        return None
    payload = decode_access_token(token)
    if payload is None or "sub" not in payload:
        return None
    return _find_user_by_subject(db, payload["sub"])