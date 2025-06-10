from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json

from app.database import SessionLocal
from app.models import Recommendation, Doctor  # Direct class imports ← [4]
from app.schemas import RecommendationCreate, RecommendationResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{doctor_id}")
def create_recommendation(doctor_id: int, payload: RecommendationCreate, db: Session = Depends(get_db)):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()  # Fixed
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    recommendation = Recommendation(  # Direct class usage
        doctor_id=doctor_id,
        patient_name=payload.patient_name,
        notes=payload.notes,
        products=json.dumps(payload.products),
        expiry=datetime.utcnow() + timedelta(days=7)
    )
    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)
    return {"link": f"/recommendation/{recommendation.uuid}"}

@router.get("/{uuid}", response_model=RecommendationResponse)
def get_recommendation(uuid: str, db: Session = Depends(get_db)):
    recommendation = db.query(Recommendation).filter(Recommendation.uuid == uuid).first()  # Fixed
    if not recommendation or recommendation.expiry < datetime.utcnow():
        raise HTTPException(status_code=404, detail="Link expired or not found")
    return RecommendationResponse(
        patient_name=recommendation.patient_name,
        notes=recommendation.notes,
        products=json.loads(recommendation.products),
        expiry=recommendation.expiry
    )
