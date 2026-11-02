from sqlalchemy import BigInteger, Column, Integer, String, JSON
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    password_hash = Column(String, nullable=True)
    # БЫЛО: role = Column(String, nullable=False, default="author")
    # СТАЛО:
    roles = Column(JSON, nullable=False, default=lambda: ["client"])
    name = Column(String, nullable=False)

    # Telegram OAuth
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=True)
    telegram_username = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
