from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  # Senha necessária para registro

class UserResponse(UserBase):
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: EmailStr
    id: int
    name: str

class LoginRequest(BaseModel):
    email: str
    password: str