import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.get_json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_home(client):
    r = client.get("/")
    assert r.status_code == 200
    data = r.get_json()
    assert data["version"] == "2.0.0"
    assert "message" in data
    assert "timestamp" in data

def test_products(client):
    r = client.get("/products")
    assert r.status_code == 200
    products = r.get_json()
    assert len(products) >= 2
    for p in products:
        assert p["price"] > 0, f"Hind peab olema positiivne! Leitud: {p['price']}"

def test_version_endpoint(client):
    r = client.get("/api/version")
    assert r.status_code == 200
    data = r.get_json()
    assert data["version"] == "2.0.0"
    assert "build" in data

def test_status_endpoint(client):
    r = client.get("/api/status")
    assert r.status_code == 200
    data = r.get_json()
    assert data["api"] == "running"
    assert "/products" in data["endpoints"]
