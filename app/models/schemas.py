from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    tier: Optional[str] = "free"


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    user_id: str
    username: str
    tier: str
    email: Optional[EmailStr]


class UsageItem(BaseModel):
    user_id: str
    count: int


class AnalyticsUsageResponse(BaseModel):
    by_user: List[UsageItem]


class TopUsersResponse(BaseModel):
    top_users: List[UsageItem]


class CurrentLimitResponse(BaseModel):
    limit: int
    remaining: int
    reset: int


class SetTierRequest(BaseModel):
    tier: str
