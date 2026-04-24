# FIXES.md — Bug Documentation

## api/main.py

### Bug 1 — Hardcoded Redis host
- **Line:** 6
- **Problem:** `redis.Redis(host="localhost")` — inside a Docker container, `localhost` refers to the container itself, not the Redis service. Connection will always fail.
- **Fix:** Changed to `host=os.getenv("REDIS_HOST", "redis")` to use the Docker service name via environment variable.

### Bug 2 — Hardcoded Redis port
- **Line:** 6
- **Problem:** `port=6379` hardcoded as an integer literal. Not configurable across environments.
- **Fix:** Changed to `port=int(os.getenv("REDIS_PORT", 6379))` to read from environment variable.

### Bug 3 — Missing /health endpoint
- **Line:** N/A
- **Problem:** No health check endpoint existed. Required for Docker HEALTHCHECK and depends_on condition checks in docker-compose.
- **Fix:** Added `GET /health` endpoint returning `{"status": "ok"}`.

## worker/worker.py

### Bug 4 — Hardcoded Redis host
- **Line:** 5
- **Problem:** Same as Bug 1 — `host="localhost"` fails inside a container.
- **Fix:** Changed to `host=os.getenv("REDIS_HOST", "redis")`.

### Bug 5 — Hardcoded Redis port
- **Line:** 5
- **Problem:** Same as Bug 2 — port hardcoded, not configurable.
- **Fix:** Changed to `port=int(os.getenv("REDIS_PORT", 6379))`.

### Bug 6 — No error handling in worker loop
- **Line:** 11-15
- **Problem:** `r.brpop()` throws an exception if Redis is unavailable. No try/except means the worker crashes permanently on any Redis hiccup.
- **Fix:** Wrapped the loop body in try/except with a 3-second retry delay.

### Bug 7 — Unused import
- **Line:** 4
- **Problem:** `import signal` is imported but never used anywhere in the file.
- **Fix:** Removed the unused import.

## frontend/app.js

### Bug 8 — Hardcoded API URL
- **Line:** 5
- **Problem:** `API_URL = "http://localhost:8000"` — localhost does not resolve to the API service inside Docker. Requests will fail.
- **Fix:** Changed to `process.env.API_URL || "http://api:8000"`.

### Bug 9 — Hardcoded port
- **Line:** 28
- **Problem:** `app.listen(3000)` — port hardcoded, not configurable across environments.
- **Fix:** Changed to `process.env.PORT || 3000`.

### Bug 10 — Missing /health endpoint
- **Line:** N/A
- **Problem:** No health check endpoint. Required for Docker HEALTHCHECK instruction.
- **Fix:** Added `GET /health` endpoint returning `{"status": "ok"}`.

## api/requirements.txt & worker/requirements.txt

### Bug 11 — Unpinned dependencies
- **Line:** All lines
- **Problem:** No version pins on any package. Silent breaking updates can occur at any time.
- **Fix:** Pinned all packages to specific versions:
  - `fastapi==0.104.1`
  - `uvicorn==0.24.0`
  - `redis==5.0.1`
