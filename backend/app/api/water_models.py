from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import WaterObject, WaterQuality
from app.schemas.water_schemas import QualityFilter
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


@router.post("/search-by-quality")
def search_by_quality(
    filter: QualityFilter,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.get("sub") != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    
    # Начинаем с базовой таблицы WaterObject и присоединяем качество воды
    query = db.query(WaterObject).join(WaterQuality)
    
    # Проходим по каждому параметру в фильтре
    for param_name, param_value in filter.model_dump(exclude_none=True).items():
        column = getattr(WaterQuality, param_name)
        
        if isinstance(param_value, list):  # [5, 10] = диапазон
            query = query.filter(column >= param_value[0])
            query = query.filter(column <= param_value[1])
        else:  # 5 = точное значение
            query = query.filter(column == param_value)
    
    return query.all()
