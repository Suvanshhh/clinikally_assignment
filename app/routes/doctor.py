from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Doctor, Review
from app.schemas import DoctorCreate, ReviewCreate, DoctorResponse
from typing import List
from fastapi.security import OAuth2PasswordBearer
from app.jwt_utils import verify_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)  
    if not payload or not payload.get("is_doctor"):
        raise HTTPException(status_code=401, detail="Invalid token or insufficient permissions")
    return payload  

@router.post("/", response_model=DoctorResponse)
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)  # Expect dict now
):
    db_doctor = Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@router.post("/{doctor_id}/review")
def review_doctor(
    doctor_id: int,
    review: ReviewCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)  # Correct type
):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    new_review = Review(
        doctor_id=doctor_id,
        rating=review.rating,
        review=review.review
    )
    db.add(new_review)
    db.commit()
    
    reviews = db.query(Review).filter(Review.doctor_id == doctor_id).all()
    avg_rating = sum(r.rating for r in reviews)/len(reviews) if reviews else 0
    db_doctor.average_rating = avg_rating
    db.commit()
    
    return {"message": "Review added successfully"}

@router.get("/", response_model=List[DoctorResponse])
def get_doctors(
    min_rating: float = 0.0,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
 
    doctors = db.query(Doctor).filter(Doctor.average_rating >= min_rating
        ).offset(skip).limit(limit).all()
    
    
    response_data = []
    for doctor in doctors:
        response_data.append({
            "id": doctor.id,
            "name": doctor.name,
            "specialization": doctor.specialization,
            "average_rating": doctor.average_rating,
            "reviews": [rev.review for rev in doctor.reviews]
        })
    
    return response_data
