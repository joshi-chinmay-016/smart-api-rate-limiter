import uuid
from fastapi import HTTPException, status

from app.core import redis_client
from app.core.security import hash_password, verify_password


async def create_user(username: str, email: str, password: str, tier: str = "free") -> dict:
    existing_id = await redis_client.redis.get(f"username:{username}")
    if existing_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    user_id = str(uuid.uuid4())
    hashed = hash_password(password)
    user_key = f"user:{user_id}"

    await redis_client.redis.hset(user_key, mapping={
        "username": username,
        "email": email,
        "password": hashed,
        "tier": tier,
    })

    await redis_client.redis.set(f"username:{username}", user_id)

    return {"user_id": user_id, "username": username, "tier": tier, "email": email}


async def authenticate_user(username: str, password: str) -> dict:
    user_id = await redis_client.redis.get(f"username:{username}")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    user_key = f"user:{user_id}"
    user = await redis_client.redis.hgetall(user_key)
    if not user or not verify_password(password, user.get("password", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return {"user_id": user_id, "username": username, "tier": user.get("tier", "free"), "email": user.get("email")}


async def get_user_by_id(user_id: str) -> dict:
    user = await redis_client.redis.hgetall(f"user:{user_id}")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


async def set_user_tier(user_id: str, tier: str) -> dict:
    user_key = f"user:{user_id}"
    if not await redis_client.redis.exists(user_key):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await redis_client.redis.hset(user_key, "tier", tier)
    return {"user_id": user_id, "tier": tier}
