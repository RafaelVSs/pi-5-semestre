# Em config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from pathlib import Path

try:
    project_root = Path(__file__).resolve().parent.parent.parent # Ajuste conforme sua estrutura
    env_path = project_root / ".env"
    if not env_path.exists():
        project_root_alt = Path(__file__).resolve().parent
        env_path_alt = project_root_alt / ".env"
        if env_path_alt.exists():
            env_path = env_path_alt
        else:
            print(f"Arquivo .env não encontrado em {env_path} ou {env_path_alt}")
except Exception as e:
    print(f"Erro ao determinar o caminho do .env: {e}")
    env_path = None


class Settings(BaseSettings):
    # Configurações do Projeto
    PROJECT_NAME: str
    API_V1_STR: str

    # Configurações JWT
    SECRET_KEY: SecretStr
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Configurações do Banco de Dados
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: str

    model_config = SettingsConfigDict(
        env_file=env_path if env_path and env_path.exists() else None,
        env_file_encoding='utf-8',
        extra='ignore'
    )

# Instância global para fácil acesso
try:
    settings = Settings()
except Exception as e:
    print(f"ERRO AO CARREGAR CONFIGURAÇÕES: Verifique seu arquivo .env ou variáveis de ambiente.")
    print(f"Detalhes do erro: {e}")
    print(f"Verifique se o arquivo .env está em: {env_path} e se todas as variáveis obrigatórias estão definidas.")
    raise