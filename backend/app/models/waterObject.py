from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db import Base
from sqlalchemy.sql import func

class WaterObject(Base):
    __tablename__ = "water_objects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    region = Column(String, nullable=False)
    type = Column(String, default="lake")

    # Связь с таблицей качества воды
    qualities = relationship("WaterQuality", back_populates="object", cascade="all, delete-orphan")


class WaterQuality(Base):
    __tablename__ = "water_quality"

    id = Column(Integer, primary_key=True, index=True)
    water_object_id = Column(Integer, ForeignKey("water_objects.id", ondelete="CASCADE"))

    Z = Column(Integer)
    H = Column(Integer)
    G = Column(Integer)
    A = Column(Integer)
    D = Column(Integer)
    W = Column(Integer)
    T = Column(Integer)
    Tw = Column(Integer)
    pH = Column(Integer)
    O = Column(Integer)
    I = Column(String)
    M = Column(Integer)
    Thw = Column(Integer)
    Ka = Column(Integer)
    SAR = Column(Integer)
    IIWP_Dc = Column(Integer)
    Tr = Column(Integer)
    Fl = Column(Integer)
    Fa = Column(Integer)

    created_at = Column(DateTime, server_default=func.now())

    object = relationship("WaterObject", back_populates="qualities")
