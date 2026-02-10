from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import WaterObject, WaterQuality
from app.schemas.water_schemas import QualityFilter
from app.api.auth import get_current_user
from app.models.water_object import WaterObject
from app.models.water_quality import WaterQuality

router = APIRouter(
    prefix="/water-objects",
    tags=["Water Objects"]
)

# ------------------------
# Получить все озёра
# ------------------------
from sqlalchemy import text
from fastapi import Depends
from sqlalchemy.orm import Session


@router.get("")
def get_all_lakes(db: Session = Depends(get_db)):
    sql = text("""
        SELECT 
            wo.id, wo.name, wo.region, wo.latitude, wo.longitude, wq."Z"
        FROM water_objects wo
        LEFT JOIN LATERAL (
            SELECT "Z" FROM water_quality 
            WHERE water_object_id = wo.id 
            ORDER BY created_at DESC 
            LIMIT 1
        ) wq ON true
        ORDER BY wo.id;
    """)
    return db.execute(sql).mappings().all()

# ------------------------
# Поиск озёр
# ------------------------
@router.get("/search")
def search_lakes(
    q: str = Query(..., min_length=2),
    # current_user=Depends(get_current_user),  # закомментировали
    db: Session = Depends(get_db)
):
    # if current_user.get("sub") != "admin":
    #     raise HTTPException(status_code=403, detail="Forbidden")

    return (
        db.query(WaterObject)
        .filter(WaterObject.name.ilike(f"%{q}%"))
        .all()
    )

@router.post("/search-by-quality")
def search_by_quality(
    filter: QualityFilter,
    db: Session = Depends(get_db)
):
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



@router.get("/{water_object_id}")
def water_object_details(
    water_object_id: int,
    db: Session = Depends(get_db)
):
    water_object = (
        db.query(WaterObject)
        .filter(WaterObject.id == water_object_id)
        .first()
    )

    if not water_object:
        raise HTTPException(status_code=404, detail="Water object not found")
    
    quality = (
        db.query(WaterQuality)
        .filter(WaterQuality.water_object_id == water_object_id)
        .first()
    )
    return {
        "id": water_object.id,
        "name": water_object.name,
        "region": water_object.region,
        "latitude": water_object.latitude,
        "longitude": water_object.longitude,
        "description": water_object.description,
        "water_quality": quality
    }

# ------------------------
# Добавление показателей воды
# ------------------------
@router.post("/{water_object_id}/quality")
def add_water_quality(
    water_object_id: int,
    data: dict,  # ожидаем все поля Z, H, G ... Fa
    db: Session = Depends(get_db)
):
    # проверяем, что такой водный объект существует
    water_obj = db.query(WaterObject).filter(WaterObject.id == water_object_id).first()
    if not water_obj:
        raise HTTPException(status_code=404, detail="Water object not found")

    # создаём объект WaterQuality
    quality = WaterQuality(
        water_object_id=water_object_id,
        Z=data.get("Z"),
        H=data.get("H"),
        G=data.get("G"),
        A=data.get("A"),
        D=data.get("D"),
        W=data.get("W"),
        T=data.get("T"),
        Tw=data.get("Tw"),
        pH=data.get("pH"),
        O=data.get("O"),
        I=data.get("I"),
        M=data.get("M"),
        Thw=data.get("Thw"),
        Ka=data.get("Ka"),
        SAR=data.get("SAR"),
        IIWP_Dc=data.get("IIWP_Dc"),
        Tr=data.get("Tr"),
        Fl=data.get("Fl"),
        Fa=data.get("Fa")
    )

    db.add(quality)
    db.commit()
    db.refresh(quality)

    return {"message": "Water quality added", "data": quality}
