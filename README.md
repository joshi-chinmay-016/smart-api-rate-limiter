# Smart API Rate Limiter

A production-grade FastAPI service implementing per-user JWT rate limiting with Redis, analytics, Prometheus/Grafana metrics, and Docker deployment.

## 🌐 Live Demo
https://api-rate-limiter-coz0.onrender.com/docs

## Folder Structure

- `app/`
  - `main.py`
  - `core/`
    - `config.py`
    - `security.py`
    - `redis_client.py`
    - `rate_limiter.py`
  - `api/`
    - `auth.py`
    - `analytics.py`
    - `protected.py`
  - `models/`
    - `schemas.py`
  - `services/`
    - `user_service.py`
    - `analytics_service.py`
  - `utils/`
    - `logger.py`
- `docker/`
  - `nginx/nginx.conf`
  - `prometheus/prometheus.yml`
- `tests/` (pytest integration tests)
- `Dockerfile`
- `docker-compose.yml`
- `requirements.txt`

## Setup Instructions

1. Install local Python requirements:

   ```bash
   python -m pip install -r requirements.txt
   ```

2. Run services locally with Docker Compose:

   ```bash
   docker-compose up --build
   ```

3. Default endpoints:
   - `POST /register`
   - `POST /login`
   - `GET /protected`
   - `GET /analytics/usage`
   - `GET /analytics/top-users`
   - `GET /analytics/current-limit`
   - `/metrics` for Prometheus

4. Monitoring
   - Prometheus: `http://localhost:9090`
   - Grafana: `http://localhost:3000` (default admin/admin)
   - Nginx proxy: `http://localhost` (forwarded to FastAPI)

## Quick API Demo (curl)

1. Register

```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"bob","email":"bob@example.com","password":"pass123","tier":"free"}'
```

2. Login

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"bob","password":"pass123"}'
```

3. Call protected route

```bash
TOKEN=<insert-token>
curl -X GET http://localhost:8000/protected \
  -H "Authorization: Bearer $TOKEN"
```

4. Analytics

```bash
curl http://localhost:8000/analytics/usage
curl http://localhost:8000/analytics/top-users
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/analytics/current-limit
```

## Running tests

```bash
pytest -q
```


