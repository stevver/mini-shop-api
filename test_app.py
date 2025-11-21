import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.get_json()['status'] == 'healthy'

def test_home(client):
    resp = client.get('/')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['version'] == '1.0.0'
    assert 'message' in data

def test_products(client):
    resp = client.get('/products')
    assert resp.status_code == 200
    products = resp.get_json()
    assert len(products) == 2
    for p in products:
        assert p['price'] > 0

def test_version_endpoint(client):
    resp = client.get('/api/version')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['version'] == '1.0.0'

def test_status_endpoint(client):
    resp = client.get('/api/status')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['api'] == 'running'
    assert '/products' in data['endpoints']
