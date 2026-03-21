import pytest
from app.core import redis_client
from fakeredis.aioredis import FakeRedis


@pytest.fixture(autouse=True)
async def mock_redis():
    """Replace real Redis with FakeRedis for all tests."""
    redis_client.redis = FakeRedis(decode_responses=True)
    await redis_client.redis.flushdb()
    yield
    await redis_client.redis.flushdb()
