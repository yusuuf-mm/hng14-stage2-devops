# HNG Stage 2 — Job Processing System

A containerized microservices application consisting of a frontend, API, and worker backed by Redis.

## Architecture

```
Internet
    │
    ▼
Frontend (Node.js :3000)
    │
    ▼
API (FastAPI :8000)
    │
    ▼
Redis (:6379) ←── Worker (Python)
```

## Prerequisites

- Docker >= 24.0
- Docker Compose >= 2.0
- Git

## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/yusuuf-mm/hng14-stage2-devops.git
cd hng14-stage2-devops
```

### 2. Create your .env file
```bash
cp .env.example .env
```

### 3. Bring the stack up
```bash
docker compose up -d --build
```

### 4. Verify all services are healthy
```bash
docker compose ps
```

Expected output — all services should show `healthy`:
```
NAME         STATUS
api          Up (healthy)
frontend     Up (healthy)
redis        Up (healthy)
worker       Up (healthy)
```

### 5. Access the application
Open your browser at: `http://localhost:3000`

## Services

| Service  | Port | Description                        |
|----------|------|------------------------------------|
| Frontend | 3000 | Job submission UI                  |
| API      | 8000 | FastAPI job management (internal)  |
| Worker   | -    | Job processor (internal)           |
| Redis    | -    | Message queue (internal only)      |

## Environment Variables

See `.env.example` for all required variables.

| Variable       | Default            | Description              |
|----------------|--------------------|--------------------------|
| REDIS_HOST     | redis              | Redis service hostname   |
| REDIS_PORT     | 6379               | Redis port               |
| API_URL        | http://api:8000    | API URL for frontend     |
| FRONTEND_PORT  | 3000               | Frontend exposed port    |

## CI/CD Pipeline

GitHub Actions pipeline runs on every push:

```
lint → test → build → security scan → integration test → deploy
```

- **Lint:** flake8 (Python), eslint (JavaScript), hadolint (Dockerfiles)
- **Test:** pytest with Redis mocked, coverage report uploaded as artifact
- **Build:** Images built and pushed to local registry, tagged with git SHA and latest
- **Security:** Trivy scan on all images, fails on CRITICAL findings
- **Integration:** Full stack brought up, job submitted and polled to completion
- **Deploy:** Rolling update on push to main only

## Stopping the Stack

```bash
docker compose down -v
```

## Running Tests Locally

```bash
pip install fastapi uvicorn redis pytest pytest-cov httpx
pytest api/tests/ -v --cov=api
```

## Author

- **Name:** Yusuf Muhammad Musa
- **Email:** yusuf2000mm@gmail.com
- **GitHub:** https://github.com/yusuuf-mm