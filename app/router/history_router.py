from ast import Param

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from ..db.database import get_db
from ..schemas.history_schema import HistoryResponse, HistoryCreate, PaginatedHistoryResponse
from ..services.history_service import HistoryService



router = APIRouter(prefix="/history", tags=["History"])


@router.get("/{history_id}", response_model=HistoryResponse)
async def get_history(history_id: int, db: AsyncSession = Depends(get_db)):
    history_service = HistoryService(db)
    history = await history_service.get_history(history_id)
    if not history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History not found")
    return history

@router.get("/user/{user_id}", response_model=PaginatedHistoryResponse[HistoryResponse])
async def list_history(
        user_id: int,
        page: int = Query(1, gt=0),
        per_page: int = Query(10, gt=0, le=100),
        player_name: Optional[str] = Query(None),
        classification: Optional[str] = Query(None),
        db: AsyncSession = Depends(get_db)
):
    history_service = HistoryService(db)

    filters = {"user_id": user_id}
    if player_name:
        filters["player_name"] = player_name
    if classification:
        filters["classification"] = classification
    return await history_service.get_all_history(
        page=page,
        per_page=per_page,
        filters=filters
    )

@router.delete("/{history_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(history_id: int, db: AsyncSession = Depends(get_db)):
    history_service = HistoryService(db)
    await history_service.delete_history(history_id)