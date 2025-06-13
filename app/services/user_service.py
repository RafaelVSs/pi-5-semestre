from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from ..core.security import get_password_hash
from ..repositories.user_repository import UserRepository
from ..models.user_model import User
from ..schemas.user_schema import UserCreate, UserUpdate, PaginatedResponse, UserResponse, UserPaginatedResponse


class UserService:
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def create_user(self, user_data: UserCreate) -> User:
        existing_user = await self.repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = get_password_hash(user_data.password)
        user = User(
            name=user_data.name,
            email=user_data.email,
            password=hashed_password
        )
        return await self.repository.create(user)

    async def get_user(self, user_id: int) -> Optional[User]:
        return await self.repository.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await self.repository.get_by_email(email)

    async def get_all_users(
            self,
            page: int = 1,
            per_page: int = 10,
            filters: Optional[dict] = None
    ) -> PaginatedResponse[UserResponse]:
        items, total = await self.repository.get_all(
            page=page,
            per_page=per_page,
            filters=filters
        )

        # Converter para Pydantic V2
        user_responses = [UserResponse.model_validate(user) for user in items]

        total_pages = (total + per_page - 1) // per_page

        return PaginatedResponse[UserResponse](
            items=user_responses,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages
        )

    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        user = await self.repository.get_by_id(user_id)
        if not user:
            return None

        update_data = user_data.dict(exclude_unset=True)
        if 'password' in update_data:
            update_data['password'] = get_password_hash(update_data['password'])

        return await self.repository.update(user_id, update_data)

    async def delete_user(self, user_id: int) -> None:
        await self.repository.delete(user_id)