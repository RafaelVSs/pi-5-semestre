from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base # Corrigido import de declarative_base
from ..core.config import settings

# Use as configurações carregadas pelo Pydantic
DB_USER = settings.POSTGRES_USER
DB_PASSWORD = settings.POSTGRES_PASSWORD
DB_NAME = settings.POSTGRES_DB
DB_HOST = settings.DB_HOST
DB_PORT = settings.DB_PORT

# String de conexão para PostgreSQL assíncrono com asyncpg
# É uma boa prática codificar a senha se ela puder conter caracteres especiais,
# mas o asyncpg pode lidar com isso. Se houver problemas, use quote_plus(DB_PASSWORD).
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Cria a engine assíncrona do SQLAlchemy

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

# Cria uma fábrica de sessões (AsyncSession)
AsyncSessionLocal = sessionmaker(
    autocommit=False, # Padrão para sessionmaker
    autoflush=False,  # Padrão para sessionmaker
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False # Importante para FastAPI para que os objetos SQLAlchemy
                           # possam ser usados fora da sessão após o commit, se necessário.
)

# Cria uma classe Base para modelos declarativos
Base = declarative_base()

# Dependência para obter uma sessão do banco de dados
async def get_db() -> AsyncSession: # Adicionando type hint para clareza
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close() # Garante que a sessão seja fechada

# Imprime a string de conexão (sem a senha) para fins de log/debug ao iniciar
print(f"Conectando ao banco (config): postgresql+asyncpg://{DB_USER}:********@{DB_HOST}:{DB_PORT}/{DB_NAME}")
