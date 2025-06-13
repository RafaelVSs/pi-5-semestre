from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from ..repositories.history_repository import HistoryRepository
from ..models.history_model import History
from ..schemas.history_schema import HistoryCreate, HistoryResponse, PaginatedHistoryResponse


class HistoryService:
    def __init__(self, db: AsyncSession):
        self.repository = HistoryRepository(db)

    async def create_history(self, history_data: HistoryCreate) -> HistoryResponse:
        # Converter o Pydantic model para SQLAlchemy model
        history = History(
            player_name=history_data.player_name,
            average_rebounds=history_data.average_rebounds,
            position=history_data.position,
            average_points=history_data.average_points,
            average_assists=history_data.average_assists,
            classification=history_data.classification,
            user_id=history_data.user_id
        )

        # Agora sim pode ser persistido
        history = await self.repository.create(history)
        return HistoryResponse.model_validate(history)

    async def get_history(self, history_id: int) -> Optional[History]:
        return await self.repository.get_by_id(history_id)

    async def get_all_history(
            self,
            page: int = 1,
            per_page: int = 10,
            filters: Optional[dict] = None
    ) -> PaginatedHistoryResponse[HistoryResponse]:
        items, total = await self.repository.get_all(
            page=page,
            per_page=per_page,
            filters=filters
        )

        # Converter para Pydantic V2
        history_responses = [HistoryResponse.model_validate(history) for history in items]
        print(history_responses)
        total_pages = (total + per_page - 1) // per_page

        return PaginatedHistoryResponse[HistoryResponse](
            items=history_responses,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages
        )

    async def delete_history(self, history_id: int) -> None:
        await self.repository.delete(history_id)