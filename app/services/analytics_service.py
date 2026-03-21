from typing import List

from app.core import redis_client


async def get_total_requests_by_user(limit: int = 1000) -> List[dict]:
    data = await redis_client.redis.zrevrange("analytics:user:requests", 0, limit - 1, withscores=True)
    return [{"user_id": uid, "count": int(score)} for uid, score in data]


async def get_top_users(limit: int = 10) -> List[dict]:
    top = await redis_client.redis.zrevrange("analytics:user:requests", 0, limit - 1, withscores=True)
    return [{"user_id": uid, "count": int(score)} for uid, score in top]


async def get_current_user_limit(user_id: str):
    key = f"rate:{user_id}"
    pipeline = redis.pipeline()
    pipeline.zremrangebyscore(key, 0, int(__import__("time").time()) - 60)
    pipeline.zcard(key)
    pipeline.zrange(key, 0, 0, withscores=True)
    results = await pipeline.execute()

    count = results[1]
    oldest_ts = results[2][0][1] if results[2] else None
    return count, oldest_ts
