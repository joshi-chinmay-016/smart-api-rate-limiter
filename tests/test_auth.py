import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_register_login_flow():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        register_resp = await client.post(
            "/register",
            json={"username": "john", "email": "john@example.com", "password": "pass123", "tier": "free"},
        )
        assert register_resp.status_code == 200
        assert register_resp.json()["username"] == "john"

        login_resp = await client.post(
            "/login",
            json={"username": "john", "password": "pass123"},
        )
        assert login_resp.status_code == 200
        assert "access_token" in login_resp.json()


@pytest.mark.asyncio
async def test_invalid_login():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/login", json={"username": "nonexistent", "password": "x"})
        assert resp.status_code == 401
