from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: Optional[str]) -> bool:
    if not hashed:
        return False
    return pwd_context.verify(plain, hashed)


def create_access_token(subject: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "role": role, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None


import hashlib
import hmac as _hmac


def verify_telegram_signature(data: dict, bot_token: str) -> bool:
    """
    Проверка подписи данных от Telegram Login Widget.
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()) if k != "hash")
    secret_key = SHA256(bot_token)
    expected = HMAC_SHA256(secret_key, data_check_string)
    """
    if not bot_token:
        return False
    received_hash = data.get("hash")
    if not received_hash:
        return False

    check_items = []
    for k in sorted(data.keys()):
        if k == "hash" or data[k] is None:
            continue
        check_items.append(f"{k}={data[k]}")
    data_check_string = "\n".join(check_items)

    secret_key = hashlib.sha256(bot_token.encode("utf-8")).digest()
    expected_hash = _hmac.new(
        secret_key, data_check_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    return _hmac.compare_digest(expected_hash, received_hash)
