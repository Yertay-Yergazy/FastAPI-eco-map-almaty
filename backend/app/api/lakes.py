from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.waterObject import WaterObject
from app.schemas.lake import LakeCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/lakes")
def read_lakes(db: Session = Depends(get_db)):
    return db.query(WaterObject).all()

@router.post("/import")
def import_lakes(lakes: list[LakeCreate]):
    db: Session = next(get_db())

    lake_objects = []
    for lake_data in lakes:
        lake_obj = WaterObject(**lake_data.dict())
        lake_objects.append(lake_obj)

    db.add_all(lake_objects)
    db.commit()


    return({"status":"success","imported":len(lake_objects)})