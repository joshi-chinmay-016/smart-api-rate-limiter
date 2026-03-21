from redis.asyncio import Redis

from .config import settings


redis = Redis.from_url(settings.redis_url, decode_responses=True)
