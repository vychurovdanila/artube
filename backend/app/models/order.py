from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    artwork_id = Column(Integer, ForeignKey("artworks.id"), nullable=False, index=True)
    designer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    type = Column(String, nullable=False)                         # cashback_claim / 3d_creation_order
    status = Column(String, nullable=False, default="pending")    # pending / approved / rejected
    proof_url = Column(String, nullable=True)