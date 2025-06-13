from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.config import settings
from ..schemas.auth_schema import UserCreate, Token, LoginRequest
from ..db.database import get_db
from ..services.auth_service import AuthService
from ..core.security import create_access_token

router = APIRouter(prefix="/auth" ,tags=["Authentication"])


@router.post("/login/", response_model=Token)
async def login(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    user = await auth_service.authenticate_user(credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    data_token = {"sub": user.email, "id": user.id, "name": user.name}
    access_token = create_access_token(data=data_token, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }