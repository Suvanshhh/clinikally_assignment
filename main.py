from fastapi import FastAPI
from app.routes import doctor, recommendation
from app.database import create_db
from app.routes import auth

app = FastAPI(title="Dermatologist Review & Recommendation API")

# Initialize DB
create_db()

# My routes
app.include_router(doctor.router, prefix="/doctor", tags=["Doctor"])
app.include_router(recommendation.router, prefix="/recommendation", tags=["Recommendation"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running smoothly!"}

@app.get("/")
def root():
    return {"message": "Welcome to the Dermatologist Review & Recommendation API!"}

@app.get("/docs", include_in_schema=False)
def custom_docs():
    return {"message": "Custom documentation endpoint. Use /docs for Swagger UI."}