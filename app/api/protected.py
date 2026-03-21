from fastapi import APIRouter, Depends, Request, Response, HTTPException, status

from app.core.security import get_current_user
from app.core.rate_limiter import RateLimiter

router = APIRouter(prefix="", tags=["protected"])


@router.get("/protected")
async def protected_endpoint(request: Request, response: Response, current_user=Depends(get_current_user)):
    user_id = current_user["user_id"]
    tier = current_user.get("tier", "free")
    client_ip = request.client.host if request.client else None

    limit, remaining, reset = await RateLimiter.consume(user_id, tier, client_ip)
    if remaining < 0:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
            headers={
                "X-RateLimit-Limit": str(limit),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(reset),
            },
        )

    response.headers["X-RateLimit-Limit"] = str(limit)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    response.headers["X-RateLimit-Reset"] = str(reset)

    return {"message": "Protected data access granted", "user": current_user}
