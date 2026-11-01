from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from app.database import Base


class Artwork(Base):
    __tablename__ = "artworks"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    type = Column(String, nullable=False, index=True)         # painting / sculpture / 3d
    status = Column(String, nullable=False, default="draft")  # draft / moderation / published
    price = Column(Float, nullable=True)
    width = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    depth = Column(Float, nullable=True)
    palette = Column(JSON, nullable=True)  # список HEX-строк