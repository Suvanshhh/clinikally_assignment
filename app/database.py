# app/database.py (fixed)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 

def create_db():
    Base.metadata.create_all(bind=engine)  

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
