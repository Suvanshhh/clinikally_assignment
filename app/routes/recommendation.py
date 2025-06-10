from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json
from typing import List

from app.database import SessionLocal
from app.models import Recommendation, Doctor
from app.schemas import RecommendationCreate, RecommendationResponse
from app.utils.product_fetcher import fetch_products

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{doctor_id}", response_model=RecommendationResponse)
async def create_recommendation(
    doctor_id: int,
    payload: RecommendationCreate,
    db: Session = Depends(get_db)
):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    
    products = await fetch_products(payload.products)
    if not products or len(products) != len(payload.products):
        raise HTTPException(
            status_code=400,
            detail="One or more products not found"
        )

    
    recommendation = Recommendation(
        doctor_id=doctor_id,
        patient_name=payload.patient_name,
        notes=payload.notes,
        products=json.dumps(products),
        expiry=datetime.utcnow() + timedelta(days=7)
    )
    
    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)

    return RecommendationResponse(
        uuid=recommendation.uuid,  
        patient_name=recommendation.patient_name,
        notes=recommendation.notes,
        products=products,
        expiry=recommendation.expiry
    )

@router.get("/{uuid}", response_model=RecommendationResponse)
async def get_recommendation(uuid: str, db: Session = Depends(get_db)):
    recommendation = db.query(Recommendation).filter(
        Recommendation.uuid == uuid
    ).first()
    
    if not recommendation or recommendation.expiry < datetime.utcnow():
        raise HTTPException(
            status_code=404,
            detail="Link expired or not found"
        )
    
    try:
        products = json.loads(recommendation.products)
    except json.JSONDecodeError:
        products = []
    
    return RecommendationResponse(
        uuid=recommendation.uuid, 
        patient_name=recommendation.patient_name,
        notes=recommendation.notes,
        products=products,
        expiry=recommendation.expiry
    )
