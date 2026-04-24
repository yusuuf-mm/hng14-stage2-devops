# Build stage
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade setuptools>=78.1.0 wheel>=0.46.2 && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final stage
FROM python:3.11-slim
WORKDIR /app

# Upgrade vulnerable base packages
RUN pip install --no-cache-dir --upgrade setuptools>=78.1.0 wheel>=0.46.2

# Create non-root user
RUN useradd -m -u 1001 appuser

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy app code
COPY worker.py .

# Switch to non-root user
USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import redis, os; r = redis.Redis(host=os.getenv('REDIS_HOST','redis'), port=int(os.getenv('REDIS_PORT',6379))); r.ping()"

CMD ["python", "worker.py"]
