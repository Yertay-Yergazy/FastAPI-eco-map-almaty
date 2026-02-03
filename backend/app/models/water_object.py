from sqlalchemy import Column, Float, Integer, String, Text
from app.db import Base


class WaterObject(Base):
    __tablename__ = "water_objects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    region = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
