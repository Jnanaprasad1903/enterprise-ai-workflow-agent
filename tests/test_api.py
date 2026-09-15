import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.database.seed_data import seed_database

@pytest.fixture(scope="module", autouse=True)
def setup():
    seed_database()

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "/docs" in data["documentation"]

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["database"] == "connected"

def test_list_products():
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    products = response.json()
    assert len(products) >= 5
    # Test category filter
    filtered = client.get("/api/v1/products?category=Electronics").json()
    assert all(p["category"] == "Electronics" for p in filtered)

def test_get_product_by_id():
    response = client.get("/api/v1/products/P001")
    assert response.status_code == 200
    product = response.json()
    assert product["name"] == "Laptop Pro 16"
    assert product["price"] == 75000.0

def test_get_product_not_found():
    response = client.get("/api/v1/products/INVALID_SKU")
    assert response.status_code == 404

def test_get_order():
    response = client.get("/api/v1/orders/ORD-1001")
    assert response.status_code == 200
    order = response.json()
    assert order["order_id"] == "ORD-1001"
    assert order["customer_name"] == "Alice Johnson"
    assert order["product_name"] == "Laptop Pro 16"

def test_returns_summary():
    response = client.get("/api/v1/returns/summary")
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert data["total_returned_units"] > 0
    # First item should be highest returns: Smart Watch Active
    top_returned = data["summary"][0]
    assert top_returned["name"] == "Smart Watch Active"

def test_database_query_api():
    payload = {"sql_query": "SELECT COUNT(*) as count FROM products;"}
    response = client.post("/api/v1/database/query", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["rows_count"] == 1
    assert res["results"][0]["count"] == 7

def test_database_query_api_security():
    payload = {"sql_query": "DELETE FROM products;"}
    response = client.post("/api/v1/database/query", json=payload)
    assert response.status_code == 400
