from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List

from app.db import get_db
from app.models.water_object import WaterObject
from app.models.water_quality import WaterQuality
from app.models.user import User
from app.schemas.water_schemas import (
    QualityFilter,
    WaterObjectCreate,
    WaterObjectUpdate,
    WaterObjectResponse,
    WaterQualityCreate
)
from app.api.auth import require_manager, get_current_admin_user

router = APIRouter(
    prefix="/water-objects",
    tags=["Water Objects"]
)


# ============================================================
# READ - Публичные endpoints (доступны всем, даже гостям)
# ============================================================

@router.get("", summary="Получить все водоёмы [публичный]")
def get_all_lakes(db: Session = Depends(get_db)):
    """
    Возвращает список всех водоёмов с последним показателем Z.
    Доступен всем без авторизации.
    """
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


@router.get("/search", summary="Поиск водоёмов [публичный]")
def search_lakes(
    q: str = Query(..., min_length=2, description="Строка поиска (минимум 2 символа)"),
    db: Session = Depends(get_db)
):
    """
    Поиск водоёмов по названию.
    Доступен всем без авторизации.
    """
    return (
        db.query(WaterObject)
        .filter(WaterObject.name.ilike(f"%{q}%"))
        .all()
    )


@router.post("/search-by-quality", summary="Фильтр по качеству воды [публичный]")
def search_by_quality(
    filter: QualityFilter,
    db: Session = Depends(get_db)
):
    """
    Фильтрация водоёмов по показателям качества воды.
    Доступен всем без авторизации.
    """
    query = db.query(WaterObject).join(WaterQuality)
    
    for param_name, param_value in filter.model_dump(exclude_none=True).items():
        column = getattr(WaterQuality, param_name)
        
        if isinstance(param_value, list):  # [5, 10] = диапазон
            query = query.filter(column >= param_value[0])
            query = query.filter(column <= param_value[1])
        else:  # 5 = точное значение
            query = query.filter(column == param_value)
    
    return query.all()


@router.get("/{water_object_id}", summary="Детали водоёма [публичный]")
def water_object_details(
    water_object_id: int,
    db: Session = Depends(get_db)
):
    """
    Подробная информация о водоёме и его качестве воды.
    Доступен всем без авторизации.
    """
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
        .order_by(WaterQuality.created_at.desc())
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


@router.get("/{water_object_id}/quality", summary="Все замеры качества воды [публичный]")
def get_quality_history(
    water_object_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить все замеры качества воды для водоёма.
    Показывает id каждого замера — (Первоначального создан для удаления конкретного замера).
    """
    water_object = db.query(WaterObject).filter(WaterObject.id == water_object_id).first()
    if not water_object:
        raise HTTPException(status_code=404, detail="Water object not found")

    records = (
        db.query(WaterQuality)
        .filter(WaterQuality.water_object_id == water_object_id)
        .order_by(WaterQuality.created_at.desc())
        .all()
    )
    return records


# ============================================================
# CREATE - Создание (только Manager и Admin)
# ============================================================

@router.post("", response_model=WaterObjectResponse, summary="Создать водоём [Manager+]")
def create_water_object(
    data: WaterObjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_manager)  # 🔒 Manager или Admin
):
    """
    Создать новый водоём.
    Требует роль Manager или Admin.
    """
    water_object = WaterObject(
        name=data.name,
        region=data.region,
        latitude=data.latitude,
        longitude=data.longitude,
        description=data.description
    )
    db.add(water_object)
    db.commit()
    db.refresh(water_object)
    return water_object


# ============================================================
# UPDATE - Обновление (только Manager и Admin)
# ============================================================

@router.put("/{water_object_id}", response_model=WaterObjectResponse, summary="Обновить водоём [Manager+]")
def update_water_object(
    water_object_id: int,
    data: WaterObjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_manager)  # 🔒 Manager или Admin
):
    """
    Обновить данные водоёма (можно передать только изменяемые поля).
    Требует роль Manager или Admin.
    """
    water_object = db.query(WaterObject).filter(WaterObject.id == water_object_id).first()
    
    if not water_object:
        raise HTTPException(status_code=404, detail="Water object not found")
    
    # Обновляем только те поля, которые переданы (не None)
    update_data = data.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(water_object, field, value)
    
    db.commit()
    db.refresh(water_object)
    return water_object


@router.post("/{water_object_id}/quality", summary="Добавить показатели воды [Manager+]")
def add_water_quality(
    water_object_id: int,
    data: WaterQualityCreate,  # 🔒 Теперь Pydantic схема, а не dict
    db: Session = Depends(get_db),
    current_user: User = Depends(require_manager)  # 🔒 Manager или Admin
):
    """
    Добавить новые показатели качества воды для водоёма.
    Требует роль Manager или Admin.
    """
    water_obj = db.query(WaterObject).filter(WaterObject.id == water_object_id).first()
    if not water_obj:
        raise HTTPException(status_code=404, detail="Water object not found")

    quality = WaterQuality(
        water_object_id=water_object_id,
        **data.model_dump(exclude_none=True)
    )

    db.add(quality)
    db.commit()
    db.refresh(quality)
    return {"message": "Water quality added", "id": quality.id}


# ============================================================
# DELETE - Удаление
# ============================================================

@router.delete("/quality/{quality_id}", summary="Удалить замер качества воды [Manager+]")
def delete_water_quality(
    quality_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_manager)  # 🔒 Manager или Admin
):
    """
    Удалить конкретную запись о качестве воды по ID.
    Напрямую ищет в таблице water_quality по id.
    Требует роль Manager или Admin.
    """
    quality = db.query(WaterQuality).filter(WaterQuality.id == quality_id).first()

    if not quality:
        raise HTTPException(status_code=404, detail="Water quality record not found")

    db.delete(quality)
    db.commit()

    return {"message": f"Water quality record #{quality_id} deleted successfully"}


@router.delete("/{water_object_id}", summary="Удалить водоём [Только Admin]")
def delete_water_object(
    water_object_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin_user)  # 🔒 Только JWT Admin
):
    """
    Удалить водоём и все его данные о качестве воды.
    Требует роль Admin (JWT токен).
    """
    water_object = db.query(WaterObject).filter(WaterObject.id == water_object_id).first()
    
    if not water_object:
        raise HTTPException(status_code=404, detail="Water object not found")
    
    # Сначала удаляем связанные данные о качестве воды
    db.query(WaterQuality).filter(WaterQuality.water_object_id == water_object_id).delete()
    
    # Затем удаляем сам водоём
    db.delete(water_object)
    db.commit()
    
    return {"message": f"Water object '{water_object.name}' deleted successfully"}

