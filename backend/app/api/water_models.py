from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import WaterObject
# from app.api.auth import get_current_user  # <- закомментировали авторизацию
from app.models.water_object import WaterObject
from app.models.water_quality import WaterQuality

router = APIRouter(
    prefix="/water-objects",
    tags=["Water Objects"]
)

# ------------------------
# Получить все озёра
# ------------------------
@router.get("")
def get_all_lakes(
    # current_user=Depends(get_current_user),  # временно закомментировали
    db: Session = Depends(get_db)
):
    # Проверка на admin пока не нужна
    # if current_user.get("sub") != "admin":
    #     raise HTTPException(status_code=403, detail="Forbidden")

    return db.query(WaterObject).all()

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

# ------------------------
# Детали водного объекта
# ------------------------
@router.get("/{id}")
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
