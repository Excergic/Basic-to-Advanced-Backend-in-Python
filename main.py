from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from database import SessionLocal, engine, Base
from pwdlib import PasswordHash
from models import Users

app = FastAPI(title="Signup Endpoint")

password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Minimum length is 8 characters")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/signup", response_model=dict)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(Users.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = get_password_hash(user.password)

    new_user = Users(
        email=user.email,
        hashed_password=hashed_password,
        is_active=True,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "message": "User created successfully",
        "user_id" : new_user.id,
        "email" : new_user.email,
    }
    
