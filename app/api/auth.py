from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta

from app.models.schemas import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from app.services.user_service import create_user, authenticate_user
from app.core.security import create_access_token


router = APIRouter(prefix="", tags=["auth"])


@router.post("/register", response_model=UserResponse)
async def register(payload: RegisterRequest):
    if payload.tier not in ["free", "premium"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid tier")
    user = await create_user(payload.username, payload.email, payload.password, payload.tier)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    user = await authenticate_user(payload.username, payload.password)
    access_token_expires = timedelta(minutes=60)
    token = create_access_token(
        {"sub": user["user_id"], "username": user["username"], "tier": user.get("tier", "free")},
        expires_delta=access_token_expires,
    )
    return {"access_token": token, "token_type": "bearer", "expires_in": access_token_expires.seconds}
