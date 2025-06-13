from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, func
from typing import List, Optional
from ..models.history_model import History

class HistoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, history: History) -> History:
        self.db.add(history)
        await self.db.commit()
        await self.db.refresh(history)
        return history

    async def get_by_id(self, history_id: int) -> Optional[History]:
        result = await self.db.execute(select(History).where(History.id == history_id))
        return result.scalar_one_or_none()

    async def get_all(self, page: int = 1, per_page: int = 10, filters: Optional[dict] = None) -> tuple[List[History], int]:
        offset = (page - 1) * per_page

        query = select(History)

        if filters:
            for field, value in filters.items():
                if hasattr(History, field):
                    query = query.where(getattr(History, field) == value)

        result = await self.db.execute(query.offset(offset).limit(per_page))
        items = result.scalars().all()

        total_result = await self.db.execute(
            select(func.count()).select_from(query.subquery())
        )
        total = total_result.scalar_one()
        return items, total

    async def delete(self, history_id: int) -> None:
        stmt = delete(History).where(History.id == history_id)
        await self.db.execute(stmt)
        await self.db.commit()