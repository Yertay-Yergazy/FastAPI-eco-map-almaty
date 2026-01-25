from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import WaterObject
from app.api.auth import get_current_user

router = APIRouter(
    prefix="/water-objects",
    tags=["Water Objects"]
)

@router.get("")
def get_all_lakes(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.get("sub") != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    return db.query(WaterObject).all()

@router.get("/search")
def search_lakes(
    q: str = Query(..., min_length=2),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.get("sub") != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    return (
        db.query(WaterObject)
        .filter(WaterObject.name.ilike(f"%{q}%"))
        .all()
    )
