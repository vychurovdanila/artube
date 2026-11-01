from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    artwork_id = Column(Integer, ForeignKey("artworks.id"), nullable=False, index=True)
    file_type = Column(String, nullable=False)  # original_photo / glb / usdz / ai_interior
    url = Column(String, nullable=False)