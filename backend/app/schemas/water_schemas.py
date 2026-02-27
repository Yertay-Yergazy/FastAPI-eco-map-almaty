from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime


# ============================================================
# СХЕМЫ ДЛЯ ВОДОЁМОВ
# ============================================================

class WaterObjectCreate(BaseModel):
    """Создание нового водоёма (manager+)"""
    name: str
    region: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None


class WaterObjectUpdate(BaseModel):
    """Обновление водоёма — все поля необязательные (manager+)"""
    name: Optional[str] = None
    region: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None


class WaterObjectResponse(BaseModel):
    """Ответ с данными водоёма"""
    id: int
    name: str
    region: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True  # чтобы работало с SQLAlchemy объектами


# ============================================================
# СХЕМЫ ДЛЯ КАЧЕСТВА ВОДЫ
# ============================================================

class WaterQualityCreate(BaseModel):
    """Добавление показателей качества воды (manager+)"""
    Z: Optional[float] = None
    H: Optional[float] = None
    G: Optional[float] = None
    A: Optional[float] = None
    D: Optional[float] = None
    W: Optional[float] = None
    T: Optional[float] = None
    Tw: Optional[float] = None
    pH: Optional[float] = None
    O: Optional[float] = None
    I: Optional[float] = None
    M: Optional[float] = None
    Thw: Optional[float] = None
    Ka: Optional[float] = None
    SAR: Optional[float] = None
    IIWP_Dc: Optional[float] = None
    Tr: Optional[float] = None
    Fl: Optional[float] = None
    Fa: Optional[float] = None


# ============================================================
# СХЕМЫ ДЛЯ ФИЛЬТРАЦИИ
# ============================================================

class QualityFilter(BaseModel):
    """Фильтр по качеству воды (публичный)"""
    Z: Optional[Union[float, list]] = None
    H: Optional[Union[float, list]] = None
    G: Optional[Union[float, list]] = None
    A: Optional[Union[float, list]] = None
    D: Optional[Union[float, list]] = None
    W: Optional[Union[float, list]] = None
    T: Optional[Union[float, list]] = None
    Tw: Optional[Union[float, list]] = None
    pH: Optional[Union[float, list]] = None
    O: Optional[Union[float, list]] = None
    I: Optional[Union[float, list]] = None
    M: Optional[Union[float, list]] = None
    Thw: Optional[Union[float, list]] = None
    Ka: Optional[Union[float, list]] = None
    SAR: Optional[Union[float, list]] = None
    IIWP_Dc: Optional[Union[float, list]] = None
    Tr: Optional[Union[float, list]] = None
    Fl: Optional[Union[float, list]] = None
    Fa: Optional[Union[float, list]] = None


# Оставлено для обратной совместимости
class LakeCreate(WaterObjectCreate):
    Z: Optional[float] = None
    H: Optional[float] = None
    G: Optional[float] = None
    A: Optional[float] = None
    D: Optional[float] = None
    W: Optional[float] = None
    T: Optional[float] = None
    Tw: Optional[float] = None
    pH: Optional[float] = None
    O: Optional[float] = None
    I: Optional[float] = None
    M: Optional[float] = None
    Thw: Optional[float] = None
    Ka: Optional[float] = None
    SAR: Optional[float] = None
    IIWP_Dc: Optional[float] = None
    Tr: Optional[float] = None
    Fl: Optional[float] = None
    Fa: Optional[float] = None
