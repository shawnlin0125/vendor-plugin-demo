import pytest
from app.main import app


@pytest.fixture
def client():
    """Use FastAPI TestClient for proper ASGI support."""
    from fastapi.testclient import TestClient
    return TestClient(app)


def test_health_returns_ok(client):
    """GET /health must return 200 with status=ok."""
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "uptime_seconds" in data
    assert isinstance(data["uptime_seconds"], int)


def test_root_returns_info(client):
    """GET / must return 200 with message and endpoints."""
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert "message" in data
    assert "endpoints" in data
    assert "/cat/breeds" in data["endpoints"]


def test_cat_breeds_endpoint_returns_200(client):
    """GET /cat/breeds must return 200 (may be 502 if external API unavailable)."""
    resp = client.get("/cat/breeds?limit=5")
    assert resp.status_code in (200, 502)
    if resp.status_code == 200:
        data = resp.json()
        assert "count" in data
        assert "breeds" in data


def test_cat_images_endpoint_returns_200(client):
    """GET /cat/images must return 200 (may be 502 if external API unavailable)."""
    resp = client.get("/cat/images?limit=3")
    assert resp.status_code in (200, 502)
    if resp.status_code == 200:
        data = resp.json()
        assert "count" in data
        assert "images" in data


def test_breed_detail_not_found(client):
    """GET /cat/breeds/nonexistent returns 404."""
    resp = client.get("/cat/breeds/nonexistent_breed_id")
    assert resp.status_code == 404
