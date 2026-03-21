from fastapi import APIRouter, Depends

from app.models.schemas import AnalyticsUsageResponse, TopUsersResponse, CurrentLimitResponse, SetTierRequest
from app.services.analytics_service import get_total_requests_by_user, get_top_users, get_current_user_limit
from app.services.user_service import set_user_tier
from app.core.security import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/usage", response_model=AnalyticsUsageResponse)
async def usage():
    data = await get_total_requests_by_user()
    return {"by_user": data}


@router.get("/top-users", response_model=TopUsersResponse)
async def top_users():
    data = await get_top_users()
    return {"top_users": data}


@router.get("/current-limit", response_model=CurrentLimitResponse)
async def current_limit(current_user=Depends(get_current_user)):
    user_id = current_user["user_id"]
    count, oldest_ts = await get_current_user_limit(user_id)
    from app.core.config import settings

    tier = current_user.get("tier", "free")
    limit = settings.premium_user_limit if tier == "premium" else settings.free_user_limit
    reset = int(oldest_ts + 60 - __import__("time").time()) if oldest_ts else 60
    remaining = max(0, limit - count)
    return {"limit": limit, "remaining": remaining, "reset": reset}


@router.post("/set-tier")
async def set_tier(request: SetTierRequest, current_user=Depends(get_current_user)):
    # Simple admin authorization by username
    if current_user["username"] != "admin":
        return {"detail": "Forbidden"}
    updated = await set_user_tier(current_user["user_id"], request.tier)
    return updated
