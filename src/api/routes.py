from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from src.database.db import execute_read_query
from src.database.sql_tool import query_database, describe_database

router = APIRouter()

# -------------------------------------------------------------
# Request & Response Schemas
# -------------------------------------------------------------
class HealthResponse(BaseModel):
    status: str
    database: str
    version: str

class ProductResponse(BaseModel):
    product_id: str
    name: str
    category: str
    price: float
    stock: int
    warranty_months: int

class OrderResponse(BaseModel):
    order_id: str
    customer_id: str
    customer_name: Optional[str] = None
    product_id: str
    product_name: Optional[str] = None
    quantity: int
    unit_price: float
    total_amount: float
    status: str
    order_date: str

class QueryRequest(BaseModel):
    sql_query: str = Field(..., description="Read-only SQLite query to execute")

class QueryResponse(BaseModel):
    query: str
    rows_count: int
    results: List[Dict[str, Any]]

# -------------------------------------------------------------
# API Endpoints
# -------------------------------------------------------------

@router.get("/health", response_model=HealthResponse, tags=["System"])
def health_check():
    """System health and database connectivity check."""
    try:
        execute_read_query("SELECT 1;")
        db_status = "connected"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return HealthResponse(
        status="online",
        database=db_status,
        version="0.1.0"
    )

@router.get("/products", response_model=List[ProductResponse], tags=["Products"])
def list_products(category: Optional[str] = Query(None, description="Filter products by category")):
    """List all enterprise catalog products, optionally filtered by category."""
    if category:
        rows = execute_read_query(
            "SELECT * FROM products WHERE LOWER(category) = LOWER(?);", (category,)
        )
    else:
        rows = execute_read_query("SELECT * FROM products ORDER BY name ASC;")
    return rows

@router.get("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
def get_product(product_id: str):
    """Retrieve specifications and inventory status for a specific product ID."""
    rows = execute_read_query(
        "SELECT * FROM products WHERE product_id = ?;", (product_id,)
    )
    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{product_id}' not found."
        )
    return rows[0]

@router.get("/orders/{order_id}", response_model=OrderResponse, tags=["Orders"])
def get_order(order_id: str):
    """Retrieve detailed information about a customer order including joined product/customer names."""
    sql = """
    SELECT 
        s.order_id, s.customer_id, c.name as customer_name,
        s.product_id, p.name as product_name,
        s.quantity, s.unit_price, s.total_amount, s.status, s.order_date
    FROM sales s
    LEFT JOIN customers c ON s.customer_id = c.customer_id
    LEFT JOIN products p ON s.product_id = p.product_id
    WHERE s.order_id = ?;
    """
    rows = execute_read_query(sql, (order_id,))
    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID '{order_id}' not found."
        )
    return rows[0]

@router.get("/returns/summary", tags=["Returns"])
def get_returns_summary():
    """Retrieve aggregated return analytics including return counts by product and category."""
    sql = """
    SELECT 
        p.product_id,
        p.name,
        p.category,
        COUNT(r.return_id) as total_returns,
        SUM(r.refund_amount) as total_refunded
    FROM returns r
    JOIN products p ON r.product_id = p.product_id
    GROUP BY p.product_id, p.name, p.category
    ORDER BY total_returns DESC;
    """
    rows = execute_read_query(sql)
    return {
        "summary": rows,
        "total_returned_units": sum(row["total_returns"] for row in rows),
        "total_refund_amount": sum(row["total_refunded"] for row in rows),
    }

@router.post("/database/query", response_model=QueryResponse, tags=["Database Tool"])
def execute_sql(payload: QueryRequest):
    """
    Direct REST endpoint to execute read-only queries against the SQLite database.
    Can be called directly by n8n HTTP Request nodes.
    """
    try:
        rows = execute_read_query(payload.sql_query)
        return QueryResponse(
            query=payload.sql_query,
            rows_count=len(rows),
            results=rows
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/database/schema", tags=["Database Tool"])
def get_schema():
    """Returns database schema for tool callers or external orchestration."""
    return {"schema": describe_database()}
