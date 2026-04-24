from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Mock redis before importing app
mock_redis = MagicMock()
with patch('redis.Redis', return_value=mock_redis):
    from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_job():
    mock_redis.lpush.return_value = 1
    mock_redis.hset.return_value = 1

    response = client.post("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert len(data["job_id"]) > 0

def test_get_job_found():
    mock_redis.hget.return_value = b"queued"

    response = client.get("/jobs/test-job-123")
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == "test-job-123"
    assert data["status"] == "queued"

def test_get_job_not_found():
    mock_redis.hget.return_value = None

    response = client.get("/jobs/nonexistent-job")
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert data["error"] == "not found"

def test_create_job_returns_unique_ids():
    mock_redis.lpush.return_value = 1
    mock_redis.hset.return_value = 1

    response1 = client.post("/jobs")
    response2 = client.post("/jobs")

    assert response1.json()["job_id"] != response2.json()["job_id"]
