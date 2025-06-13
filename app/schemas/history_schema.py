from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar, List

T = TypeVar('T')

class HistoryBase(BaseModel):
    player_name: str
    average_rebounds: float
    position: str
    average_points: float
    average_assists: float
    classification: str
    user_id: int

class HistoryCreate(HistoryBase):
    pass

class HistoryResponse(HistoryBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PaginatedHistoryResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    per_page: int
    total_pages: int