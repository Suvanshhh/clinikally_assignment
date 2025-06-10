from pydantic import BaseModel, validator, ValidationError
from typing import List
from datetime import datetime

class ReviewCreate(BaseModel):
    rating: int
    review: str

    @validator('review')
    def review_max_100_words(cls, v):
        if len(v.split()) > 100:
            raise ValueError('Review must not exceed 100 words')
        return v

class DoctorBase(BaseModel):
    name: str
    specialization: str

class DoctorCreate(DoctorBase):
    pass

class DoctorResponse(DoctorBase):
    id: int
    average_rating: float
    reviews: List[str]  

    class Config:
        orm_mode = True

class Product(BaseModel):
    id: int
    title: str
    description: str
    price: float


class RecommendationCreate(BaseModel):
    patient_name: str
    notes: str
    products: List[int]  

class RecommendationResponse(BaseModel):
    uuid: str
    patient_name: str
    notes: str
    products: List[Product]
    expiry: datetime
