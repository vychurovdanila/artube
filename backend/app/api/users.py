from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/me/become-author", response_model=UserRead)
def become_author(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if "author" not in current_user.roles:
        # Принудительно создаем новый список (SQLAlchemy не видит мутацию in-place для JSON)
        current_user.roles = list(current_user.roles) + ["author"]
        db.commit()
        db.refresh(current_user)
    return current_user


@router.post("/me/become-partner", response_model=UserRead)
def become_partner(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if "partner" not in current_user.roles:
        current_user.roles = list(current_user.roles) + ["partner"]
        db.commit()
        db.refresh(current_user)
    return current_user
