from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.classification_schema import PlayerStatsInput, ClassificationResult
from ..services.classification_service import ClassificationService
from ..services.history_service import HistoryService
from ..db.database import get_db

router = APIRouter(prefix="/classification", tags=["Classification"])

# Inicialização do serviço
classification_service = ClassificationService()

@router.post("/", response_model=ClassificationResult)
async def classify_player(
    stats: PlayerStatsInput,
    player_name: str,
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    history_service = HistoryService(db)
    return await classification_service.classify_player(
        stats=stats,
        player_name=player_name,
        user_id=user_id,
        history_service=history_service
    )