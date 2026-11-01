from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)  # video / article
    content = Column(Text, nullable=True)
    cover_url = Column(String, nullable=True)