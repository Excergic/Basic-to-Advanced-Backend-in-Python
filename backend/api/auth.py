from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import AsyncSessionLocal
from backend.core.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_password_hash, verify_password
from backend.models.user import Users
from backend.schemas.auth import LoginRequest, SignupRequest, SignupResponse, Token

router = APIRouter(prefix="/api/auth", tags=["auth"])

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: SignupRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Users).where(Users.email == body.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    hashed = get_password_hash(body.password)
    user = Users(
        email=body.email,
        password_hash=hashed,
        is_verified=False,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return SignupResponse(
        message="User created successfully",
        user_id=str(user.id),
        email=user.email,
    )

@router.post("/login", response_model=Token)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Users).where(Users.email == body.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
