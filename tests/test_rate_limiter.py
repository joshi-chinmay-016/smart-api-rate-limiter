import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_rate_limiter_strict_for_free_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/register", json={"username": "bob", "email": "bob@example.com", "password": "pass123", "tier": "free"})
        login = await client.post("/login", json={"username": "bob", "password": "pass123"})
        token = login.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}
        for i in range(100):
            resp = await client.get("/protected", headers=headers)
            assert resp.status_code == 200

        resp = await client.get("/protected", headers=headers)
        assert resp.status_code == 429


@pytest.mark.asyncio
async def test_premium_user_has_more_capacity():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/register", json={"username": "alice", "email": "alice@example.com", "password": "pass123", "tier": "premium"})
        login = await client.post("/login", json={"username": "alice", "password": "pass123"})
        token = login.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}
        for i in range(100):
            resp = await client.get("/protected", headers=headers)
            assert resp.status_code == 200

        # still OK
        resp = await client.get("/protected", headers=headers)
        assert resp.status_code == 200
