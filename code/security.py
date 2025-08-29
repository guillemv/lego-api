from datetime import datetime, timedelta, timezone
from typing import List, Optional
import jwt
from jwt import InvalidTokenError  # <- para capturar errores de PyJWT
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from .settings import settings
from .deps import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    scopes={"read":"Leer recursos","write":"Crear/editar recursos","admin":"Acceso administrativo"},
)

credentials_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No autorizado",
    headers={"WWW-Authenticate": "Bearer"},
)

async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    db = Depends(get_db),
):
    if not token:
        raise credentials_exc
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub: Optional[str] = payload.get("sub")
        token_scopes: List[str] = payload.get("scopes", [])
        if sub is None:
            raise credentials_exc
    except InvalidTokenError:
        raise credentials_exc

    # Usa la DB inyectada por Depends(get_db)
    user = await db.users.find_one({"email": sub})
    if not user:
        raise credentials_exc

    # Valida scopes
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(status_code=403, detail="Permisos insuficientes")

    return user

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
