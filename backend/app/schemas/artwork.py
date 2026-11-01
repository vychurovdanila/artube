from typing import List, Optional

from pydantic import BaseModel, Field


class ArtworkCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    type: str = Field(pattern="^(painting|sculpture|3d)$")
    price: Optional[float] = Field(default=None, ge=0)
    width: Optional[float] = Field(default=None, gt=0)
    height: Optional[float] = Field(default=None, gt=0)
    depth: Optional[float] = Field(default=None, gt=0)
    palette: Optional[List[str]] = None


class ArtworkRead(BaseModel):
    id: int
    author_id: int
    title: str
    description: Optional[str]
    type: str
    status: str
    price: Optional[float]
    width: Optional[float]
    height: Optional[float]
    depth: Optional[float]
    palette: Optional[List[str]]

    model_config = {"from_attributes": True}
