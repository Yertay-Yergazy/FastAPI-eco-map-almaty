from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db import Base

class WaterQuality(Base):
    __tablename__ = "water_quality"

    id = Column(Integer, primary_key=True, index=True)
    water_object_id = Column(Integer, ForeignKey("water_objects.id"))

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
    I = Column(Integer)
    M = Column(Integer)
    Thw = Column(Integer)
    Ka = Column(Integer)
    SAR = Column(Integer)
    IIWP_Dc = Column(Integer)
    Tr = Column(Integer)
    Fl = Column(Integer)
    Fa = Column(Integer)

    created_at = Column(DateTime(timezone=False), server_default=func.now())
