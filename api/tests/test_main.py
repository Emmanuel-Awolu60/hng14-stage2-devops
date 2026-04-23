from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock redis before importing app
mock_redis = MagicMock()
mock_redis.ping.return_value = True
mock_redis.lpush.return_value = 1
mock_redis.hset.return_value = 1
mock_redis.hget.return_value = "queued"

with patch("redis.Redis", return_value=mock_redis):
    from main import app

client = TestClient(app)


def test_root_returns_running():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}


def test_health_returns_healthy():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "healthy"}


def test_create_job_returns_job_id():
    response = client.post("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert len(data["job_id"]) == 36  # UUID length


def test_get_job_returns_status():
    fake_id = "test-job-123"
    response = client.get(f"/jobs/{fake_id}")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


def test_get_nonexistent_job_returns_error():
    mock_redis.hget.return_value = None
    response = client.get("/jobs/nonexistent-id")
    assert response.status_code == 404
