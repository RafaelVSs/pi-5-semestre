from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List, Generic, TypeVar
from datetime import datetime


T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    per_page: int
    total_pages: int


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,  # Permite conversão de ORM para Pydantic
        arbitrary_types_allowed=True  # Opcional, para lidar com tipos complexos
    )
class UserPaginatedResponse(BaseModel):
    items: List[T]
    total: int
    page: int
    per_page: int
    total_pages: int