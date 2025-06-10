from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import SessionLocal
from app.jwt_utils import create_access_token

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


fake_users_db = {
    "user1": {
        "username": "user1",
        "hashed_password": pwd_context.hash("pass1"),
        "is_doctor": True 
    },
    "user2": {
        "username": "user2",
        "hashed_password": pwd_context.hash("pass2"),
        "is_doctor": False
    }
}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or not pwd_context.verify(password, user["hashed_password"]):
        return None
    return user

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    
    token_data = {
        "sub": user["username"],
        "is_doctor": user.get("is_doctor", False)  # Dynamic role ← [2]
    }
    token = create_access_token(data=token_data)
    return {"access_token": token, "token_type": "bearer"}
                       