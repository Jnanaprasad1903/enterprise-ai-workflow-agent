import pytest
from src.database.seed_data import seed_database
from src.database.sql_tool import query_database, describe_database
from src.database.db import execute_read_query

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    """Ensure clean seeded database exists before running tests."""
    seed_database()

def test_describe_database():
    """Verify that describe_database returns valid schema text."""
    schema = describe_database()
    assert "CREATE TABLE" in schema
    assert "products" in schema
    assert "sales" in schema
    assert "returns" in schema

def test_query_highest_revenue():
    """Verify query computing product with highest revenue (Scenario 1)."""
    sql = """
    SELECT p.name, SUM(s.total_amount) AS total_revenue
    FROM sales s
    JOIN products p ON s.product_id = p.product_id
    GROUP BY p.name
    ORDER BY total_revenue DESC
    LIMIT 1;
    """
    res = query_database(sql)
    assert "Laptop Pro 16" in res
    assert "450000" in res

def test_query_highest_returns():
    """Verify query identifying product with highest returns (Scenario 3 part 1)."""
    sql = """
    SELECT p.name, p.category, COUNT(r.return_id) AS return_count
    FROM returns r
    JOIN products p ON r.product_id = p.product_id
    GROUP BY p.name, p.category
    ORDER BY return_count DESC
    LIMIT 1;
    """
    res = query_database(sql)
    assert "Smart Watch Active" in res
    assert "Electronics" in res
    # 5 returns for Smart Watch Active in seeded data
    assert "5" in res

def test_blocked_destructive_query():
    """Verify that DROP or DELETE queries are rejected by security controls."""
    res = query_database("DROP TABLE products;")
    assert "Security Violation" in res

def test_syntax_error_handling():
    """Verify that SQL syntax errors return clear explanations rather than crashing."""
    res = query_database("SELECT non_existent_column FROM products;")
    assert "Database Error" in res
