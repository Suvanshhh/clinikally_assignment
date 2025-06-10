from pydantic import BaseModel, ValidationError, Field, field_validator
from typing import List, Annotated
from datetime import datetime

class ReviewCreate(BaseModel):
    rating: Annotated[int, Field(..., description="Rating must be between 1 and 5", ge=1, le=5)]
    review: Annotated[str,Field(..., description="Review text must not exceed 100 words")]

    @field_validator('review')
    @classmethod
    def review_max_100_words(cls, v):
        if len(v.split()) > 100:
            raise ValueError('Review must not exceed 100 words')
        return v

class DoctorBase(BaseModel):
    name: Annotated[str, Field(..., description="Doctor's name")]
    specialization: Annotated[str, Field(..., description="Doctor's specialization")]

class DoctorCreate(DoctorBase):
    pass

class DoctorResponse(DoctorBase):
    id: int
    average_rating: Annotated[float, Field(default=0.0, description="Average rating of the doctor")]
    reviews: Annotated[List[str], Field(default_factory=list, description="List of reviews for the doctor")]  

    class Config:
        orm_mode = True

class Product(BaseModel):
    id: int
    title: Annotated[str, Field(..., description="Product title")]
    description: Annotated[str, Field(..., description="Product description")]
    price: Annotated[float, Field(..., description="Product price")]


class RecommendationCreate(BaseModel):
    patient_name: Annotated[str, Field(..., description="Name of the patient")]
    notes: Annotated[str, Field(..., description="Notes for the recommendation")]
    products: Annotated[List[int], Field(..., description="List of product IDs to recommend")]  

class RecommendationResponse(BaseModel):
    uuid: Annotated[str, Field(..., description="Unique identifier for the recommendation")]
    patient_name: Annotated[str, Field(..., description="Name of the patient")]
    notes: Annotated[str, Field(..., description="Notes for the recommendation")]
    products: Annotated[List[Product], Field(..., description="List of recommended products")]
    expiry: datetime
