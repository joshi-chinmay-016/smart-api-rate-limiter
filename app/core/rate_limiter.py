import time
import uuid
from typing import Tuple

from .config import settings
from . import redis_client


class RateLimiter:
    WINDOW_SECONDS = 60

    @staticmethod
    async def _resolve_limit(tier: str) -> int:
        if tier == "premium":
            return settings.premium_user_limit
        return settings.free_user_limit

    @classmethod
    async def consume(cls, user_id: str, tier: str, client_ip: str = None) -> Tuple[int, int, int]:
        user_limit = await cls._resolve_limit(tier)

        now = int(time.time())
        window_start = now - cls.WINDOW_SECONDS

        user_key = f"rate:{user_id}"

        xid = str(uuid.uuid4())

        # user rate check
        await redis_client.redis.zremrangebyscore(user_key, 0, window_start)
        request_count = await redis_client.redis.zcard(user_key)

        if request_count >= user_limit:
            oldest = await redis_client.redis.zrange(user_key, 0, 0, withscores=True)
            reset = int(oldest[0][1] + cls.WINDOW_SECONDS - now) if oldest else cls.WINDOW_SECONDS
            return user_limit, -1, reset  # Return -1 to signal rejection

        await redis_client.redis.zadd(user_key, {xid: now})
        await redis_client.redis.expire(user_key, cls.WINDOW_SECONDS + 5)

        total = request_count + 1
        remaining = max(0, user_limit - total)

        # analytics counter
        await redis_client.redis.zincrby("analytics:user:requests", 1, user_id)

        # reset window from oldest existing element
        oldest = await redis_client.redis.zrange(user_key, 0, 0, withscores=True)
        reset = int(oldest[0][1] + cls.WINDOW_SECONDS - now) if oldest else cls.WINDOW_SECONDS

        return user_limit, remaining, reset
