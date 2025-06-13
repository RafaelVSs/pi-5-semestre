from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.user_service import UserService
from ..schemas.user_schema import UserCreate, UserUpdate, UserResponse, PaginatedResponse
from ..db.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    return await user_service.create_user(user)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/", response_model=PaginatedResponse[UserResponse])
async def list_users(
        page: int = Query(1, gt=0),
        per_page: int = Query(10, gt=0, le=100),
        name: Optional[str] = Query(None),
        email: Optional[str] = Query(None),
        db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)

    filters = {}
    if name:
        filters["name"] = name
    if email:
        filters["email"] = email

    return await user_service.get_all_users(
        page=page,
        per_page=per_page,
        filters=filters
    )

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    updated_user = await user_service.update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    await user_service.delete_user(user_id)