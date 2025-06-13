from datetime import timedelta
from typing import Dict, Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..core.config import settings
from ..repositories.user_repository import UserRepository
from ..core.security import verify_password, create_access_token


class AuthService:
    def __init__(self, db_session: AsyncSession):  # Recebe a sessão do banco
        self.user_repo = UserRepository(db_session)  # Passa a sessão para o UserRepository
        # self.db_session = db_session # Você pode guardar a sessão aqui também se o AuthService precisar dela diretamente

    async def authenticate_user(self, email: str, password: str):  # -> Optional[User] ou seu schema de usuário
        """
        Autentica um usuário com base no e-mail e senha.
        Retorna o objeto do usuário se a autenticação for bem-sucedida, senão None ou levanta HTTPException.
        """
        user = await self.user_repo.get_by_email(email)
        if not user:
            # Usuário não encontrado
            return None

        if not verify_password(password, user.password):
            # Senha incorreta
            return None

        return user
