# code/routers/auth.py
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Security, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr

from ..security import get_password_hash, verify_password, create_access_token, get_current_user
from ..settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    scopes: list[str] = []  # p.ej. ["read","write"]

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/users", status_code=201)
async def create_user_admin(
    user: UserCreate,
    request: Request,
    me = Security(get_current_user, scopes=["admin"]),  # <-- requiere admin
):
    db = request.app.state.db
    if await db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    hashed = get_password_hash(user.password)
    await db.users.insert_one({
        "email": user.email.lower(),
        "hashed_password": hashed,
        "scopes": user.scopes,
    })
    return {"ok": True}

@router.post("/token", response_model=Token)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    db = request.app.state.db
    user = await db.users.find_one({"email": form_data.username.lower()})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Credenciales inválidas")
    scopes = user.get("scopes", [])
    access_token = create_access_token(
        data={"sub": user["email"], "scopes": scopes},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}

