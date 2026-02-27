from pydantic import BaseModel, EmailStr, Field

class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        description="Minimum length is 8 characters",
    )

class SignupResponse(BaseModel):
    message: str
    user_id: str
    email: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
