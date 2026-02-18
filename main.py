from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from database import SessionLocal, engine, Base
from models import Users
from pwdlib import PasswordHash

app = FastAPI(title = "Signup Endpoint")

pwd_hasher = PasswordHash("bcrypt")

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length = 8, description="Minimum length is 8 characters")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

## Signup Endpoint
@app.post("/signup", response_model = dict)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    exisiting_user = db.query(Users).filter(Users.email == user.email).first()
    if exisiting_user:
        raise HTTPException(status_code = 400, detail = "User already exists")
    
    hashed_password = pwd_hasher.hash(user.password)
    
    new_user = Users(
        email = user.email,
        hashed_password = hashed_password, ## Now secure
        is_active = True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "message": "User created successfully",
        "user_id" : new_user.id,
        "email" : new_user.email,
    }
    
