import json
from typing import Dict, Any, Callable
from src.database.sql_tool import query_database, describe_database
from src.rag.rag_tool import search_policy_documents
from src.database.db import execute_read_query

def get_product_details(product_id: str) -> str:
    """
    Look up live product inventory, pricing, and warranty details by product ID (e.g. 'P001', 'P002').
    Use this when you have a specific product ID and need its catalog specs.
    """
    rows = execute_read_query("SELECT * FROM products WHERE product_id = ?;", (product_id,))
    if not rows:
        return f"Product with ID '{product_id}' not found."
    return json.dumps(rows[0], indent=2)

def get_order_details(order_id: str) -> str:
    """
    Look up detailed customer order information by order ID (e.g. 'ORD-1001').
    Returns purchaser name, product purchased, quantity, total amount, and delivery/return status.
    """
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
        return f"Order with ID '{order_id}' not found."
    return json.dumps(rows[0], indent=2)

def get_returns_summary_tool() -> str:
    """
    Returns an aggregated overview of returned items across all products and categories,
    including return frequencies and total refund dollars.
    """
    sql = """
    SELECT 
        p.product_id, p.name, p.category,
        COUNT(r.return_id) as total_returns,
        SUM(r.refund_amount) as total_refunded
    FROM returns r
    JOIN products p ON r.product_id = p.product_id
    GROUP BY p.product_id, p.name, p.category
    ORDER BY total_returns DESC;
    """
    rows = execute_read_query(sql)
    return json.dumps(rows, indent=2)

# Registry of callable Python functions for Gemini Function Calling
TOOL_FUNCTIONS = [
    query_database,
    describe_database,
    search_policy_documents,
    get_product_details,
    get_order_details,
    get_returns_summary_tool,
]

# Name-to-function lookup table for the agentic execution loop
TOOL_MAP: Dict[str, Callable] = {
    "query_database": query_database,
    "describe_database": describe_database,
    "search_policy_documents": search_policy_documents,
    "get_product_details": get_product_details,
    "get_order_details": get_order_details,
    "get_returns_summary_tool": get_returns_summary_tool,
}
