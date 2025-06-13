from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, func
from typing import List, Optional
from ..models.user_model import User

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_all(self,page: int = 1,per_page: int = 10,filters: Optional[dict] = None) -> tuple[List[User], int]:
        # Calcular offset
        offset = (page - 1) * per_page

        # Construir query base
        query = select(User)

        # Aplicar filtros se existirem
        if filters:
            for field, value in filters.items():
                if hasattr(User, field):
                    query = query.where(getattr(User, field) == value)

        result = await self.db.execute(query.offset(offset).limit(per_page))
        items = result.scalars().all()

        total_result = await self.db.execute(
            select(func.count()).select_from(query.subquery())
        )
        total = total_result.scalar_one()
        return items, total

    async def update(self, user_id: int, update_data: dict) -> Optional[User]:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(**update_data)
            .returning(User)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one_or_none()

    async def delete(self, user_id: int) -> None:
        stmt = delete(User).where(User.id == user_id)
        await self.db.execute(stmt)
        await self.db.commit()