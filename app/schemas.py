from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ReviewCreate(BaseModel):
    rating: int
    review: str

class DoctorBase(BaseModel):
    name: str
    specialization: str

class DoctorCreate(DoctorBase):
    pass

class DoctorResponse(DoctorBase):
    id: int
    average_rating: float
    reviews: List[str]  # Should match your ORM structure

    class Config:
        orm_mode = True

class RecommendationCreate(BaseModel):
    patient_name: str
    notes: str
    products: List[str]

class RecommendationResponse(BaseModel):
    patient_name: str
    notes: str
    products: List[str]
    expiry: datetime
