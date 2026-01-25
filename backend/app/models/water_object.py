from sqlalchemy import Column, Integer, String
from app.db import Base

class WaterObject(Base):
    __tablename__ = "water_objects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    region = Column(String, nullable=False)
