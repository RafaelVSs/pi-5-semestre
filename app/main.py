import uvicorn
from fastapi import FastAPI
from .db.database import engine, Base
from .router.user_router import router as router_user
from .router.auth_router import router as router_auth
from .router.history_router import router as router_history
from .router.classification_router import router as router_classification
from .core.config import settings

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_prefix=settings.API_V1_STR
)

@app.on_event("startup")  # Evento que ocorre na inicialização do aplicativo
async def startup_event():
    await create_tables()  # Chama a função para criar as tabelas

app.include_router(router_user)
app.include_router(router_auth)
app.include_router(router_history)
app.include_router(router_classification)
