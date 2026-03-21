from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Smart API Rate Limiter"
    redis_url: str = "redis://redis:6379/0"
    secret_key: str = "change-me-to-a-secure-secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    free_user_limit: int = 100
    premium_user_limit: int = 1000
    ip_fallback_limit: int = 60

    prometheus_enabled: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
