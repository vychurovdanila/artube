from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_role
from app.api.deps import get_current_user_optional
from app.models.artwork import Artwork
from app.models.user import User
from app.schemas.artwork import ArtworkCreate, ArtworkRead

router = APIRouter(prefix="/api/artworks", tags=["artworks"])


@router.post("", response_model=ArtworkRead, status_code=status.HTTP_201_CREATED)
def create_artwork(
    payload: ArtworkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("author")),
):
    artwork = Artwork(
        author_id=current_user.id,
        title=payload.title,
        description=payload.description,
        type=payload.type,
        status="draft",
        price=payload.price,
        width=payload.width,
        height=payload.height,
        depth=payload.depth,
        palette=payload.palette,
    )
    db.add(artwork)
    db.commit()
    db.refresh(artwork)
    return artwork


@router.get("", response_model=List[ArtworkRead])
def list_artworks(
    db: Session = Depends(get_db),
    type: Optional[str] = Query(default=None, pattern="^(painting|sculpture|3d)$"),
    status_filter: Optional[str] = Query(
        default="published", alias="status", pattern="^(draft|moderation|published)$"
    ),
    price_min: Optional[float] = Query(default=None, ge=0),
    price_max: Optional[float] = Query(default=None, ge=0),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
):
    q = db.query(Artwork)
    if type is not None:
        q = q.filter(Artwork.type == type)
    if status_filter is not None:
        q = q.filter(Artwork.status == status_filter)
    if price_min is not None:
        q = q.filter(Artwork.price >= price_min)
    if price_max is not None:
        q = q.filter(Artwork.price <= price_max)
    return q.order_by(Artwork.id.desc()).offset(skip).limit(limit).all()


@router.get("/{artwork_id}", response_model=ArtworkRead)
def get_artwork(
    artwork_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    artwork = db.query(Artwork).filter(Artwork.id == artwork_id).first()
    if artwork is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artwork not found")
    # Черновики и модерация видны только владельцу
    if artwork.status != "published":
        if current_user is None or current_user.id != artwork.author_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artwork not found")
    return artwork
