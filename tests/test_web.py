from fastapi.testclient import TestClient
from app.web import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["product"] == "KaagazEdge"
    assert "invoice" in body["schemas"]


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "KaagazEdge" in response.text
