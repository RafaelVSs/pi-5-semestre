# app/core/security.py
from datetime import datetime, timedelta, timezone
from typing import Optional, Any

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from ..schemas.auth_schema import TokenPayload
from app.core.config import settings


# Configuração do hashing de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    secret_key_str = settings.SECRET_KEY.get_secret_value()
    encoded_jwt = jwt.encode(to_encode, secret_key_str, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[TokenPayload]:
    try:
        secret_key_str = settings.SECRET_KEY.get_secret_value()
        payload = jwt.decode(token, secret_key_str, algorithms=[settings.ALGORITHM])


        email: Optional[str] = payload.get("sub")
        user_id: Optional[int] = payload.get("id")
        name: Optional[str] = payload.get("nome")


        if email is None or user_id is None or name is None:
            # Poderia levantar uma exceção aqui se um campo essencial estiver faltando
            return None

        return TokenPayload(sub=EmailStr(email), id=user_id, name=name)

    except JWTError:  # Se o token for inválido (expirado, assinatura incorreta, etc.)
        return None