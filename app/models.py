from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from app.database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    specialization = Column(String)
    average_rating = Column(Float, default=0.0)

    reviews = relationship("Review", back_populates="doctor")
    recommendations = relationship("Recommendation", back_populates="doctor")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    rating = Column(Integer)
    review = Column(Text)

    doctor = relationship("Doctor", back_populates="reviews")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, default=lambda: str(uuid4()))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    patient_name = Column(String)
    notes = Column(Text)
    products = Column(Text)
    expiry = Column(DateTime)

    doctor = relationship("Doctor", back_populates="recommendations")
