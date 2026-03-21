import uvicorn
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.auth import router as auth_router
from app.api.analytics import router as analytics_router
from app.api.protected import router as protected_router
from app.core.redis_client import redis
from contextlib import asynccontextmanager
from app.utils.logger import configure_logging


configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await redis.ping()
    yield
    # Shutdown
    await redis.close()


app = FastAPI(title="Smart API Rate Limiter", lifespan=lifespan)

# Add Prometheus instrumentation before routing
Instrumentator().instrument(app).expose(app)

app.include_router(auth_router)
app.include_router(analytics_router)
app.include_router(protected_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
