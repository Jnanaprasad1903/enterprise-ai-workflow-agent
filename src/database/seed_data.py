import sqlite3
from pathlib import Path
from typing import Optional
from src.config import DATABASE_PATH
from src.database.db import get_connection, init_db

PRODUCTS = [
    ("P001", "Laptop Pro 16", "Electronics", 75000.0, 45, 24),
    ("P002", "Smart Watch Active", "Electronics", 12000.0, 150, 12),
    ("P003", "Ergonomic Office Chair", "Furniture", 18000.0, 80, 36),
    ("P004", "Noise-Cancelling Headphones", "Electronics", 15000.0, 90, 12),
    ("P005", "Mechanical Keyboard", "Accessories", 6500.0, 200, 12),
    ("P006", "Ultra-Wide 4K Monitor", "Electronics", 42000.0, 60, 36),
    ("P007", "Standing Desk Converter", "Furniture", 22000.0, 40, 60),
]

CUSTOMERS = [
    ("C001", "Alice Johnson", "alice@enterprise.com", "VIP", "2025-01-10"),
    ("C002", "Bob Smith", "bob@techcorp.io", "Standard", "2025-01-15"),
    ("C003", "Charlie Davis", "charlie@fintech.net", "VIP", "2025-02-01"),
    ("C004", "Diana Prince", "diana@designlab.org", "Standard", "2025-02-10"),
    ("C005", "Evan Wright", "evan@consulting.biz", "Standard", "2025-03-01"),
]

SALES = [
    # order_id, customer_id, product_id, quantity, unit_price, total_amount, status, order_date
    ("ORD-1001", "C001", "P001", 3, 75000.0, 225000.0, "Completed", "2026-08-05"),
    ("ORD-1002", "C002", "P002", 4, 12000.0, 48000.0, "Returned", "2026-08-08"),
    ("ORD-1003", "C003", "P003", 2, 18000.0, 36000.0, "Completed", "2026-08-10"),
    ("ORD-1004", "C004", "P001", 2, 75000.0, 150000.0, "Completed", "2026-08-12"),
    ("ORD-1005", "C005", "P002", 3, 12000.0, 36000.0, "Returned", "2026-08-14"),
    ("ORD-1006", "C001", "P004", 2, 15000.0, 30000.0, "Completed", "2026-08-16"),
    ("ORD-1007", "C002", "P005", 5, 6500.0, 32500.0, "Completed", "2026-08-18"),
    ("ORD-1008", "C003", "P006", 2, 42000.0, 84000.0, "Completed", "2026-08-20"),
    ("ORD-1009", "C004", "P002", 5, 12000.0, 60000.0, "Returned", "2026-08-22"),
    ("ORD-1010", "C005", "P007", 1, 22000.0, 22000.0, "Completed", "2026-08-25"),
    ("ORD-1011", "C001", "P002", 2, 12000.0, 24000.0, "Returned", "2026-08-28"),
    ("ORD-1012", "C003", "P001", 1, 75000.0, 75000.0, "Completed", "2026-09-01"),
    ("ORD-1013", "C002", "P004", 1, 15000.0, 15000.0, "Returned", "2026-09-02"),
    ("ORD-1014", "C004", "P002", 3, 12000.0, 36000.0, "Returned", "2026-09-05"),
    ("ORD-1015", "C005", "P003", 1, 18000.0, 18000.0, "Returned", "2026-09-07"),
    ("ORD-1016", "C001", "P006", 3, 42000.0, 126000.0, "Completed", "2026-09-10"),
]

RETURNS = [
    # return_id, order_id, product_id, customer_id, reason, status, return_date, refund_amount
    ("RET-2001", "ORD-1002", "P002", "C002", "Defective battery: shuts down within 2 hours", "Refunded", "2026-08-11", 48000.0),
    ("RET-2002", "ORD-1005", "P002", "C005", "Bluetooth fails to pair with Android devices", "Refunded", "2026-08-17", 36000.0),
    ("RET-2003", "ORD-1009", "P002", "C004", "Battery drain and excessive heating during charge", "Refunded", "2026-08-25", 60000.0),
    ("RET-2004", "ORD-1011", "P002", "C001", "Screen flickering and unresponsive touchscreen", "Refunded", "2026-08-30", 24000.0),
    ("RET-2005", "ORD-1013", "P004", "C002", "Right ear cup crackles under active noise cancellation", "Refunded", "2026-09-05", 15000.0),
    ("RET-2006", "ORD-1014", "P002", "C004", "Step tracker inaccurate and water seal condensation", "Refunded", "2026-09-08", 36000.0),
    ("RET-2007", "ORD-1015", "P003", "C005", "Lumbar support adjustment knob broken on arrival", "Refunded", "2026-09-10", 18000.0),
]

def seed_database(db_path: Optional[Path] = None) -> None:
    """Initializes schema and populates clean business data."""
    target_path = db_path or DATABASE_PATH
    print(f"[*] Initializing database at: {target_path}")
    init_db(target_path)
    
    conn = get_connection(target_path)
    try:
        with conn:
            # Clear existing data to ensure idempotent seeding
            conn.execute("DELETE FROM returns;")
            conn.execute("DELETE FROM sales;")
            conn.execute("DELETE FROM customers;")
            conn.execute("DELETE FROM products;")
            
            # Insert Products
            conn.executemany(
                "INSERT INTO products (product_id, name, category, price, stock, warranty_months) VALUES (?, ?, ?, ?, ?, ?);",
                PRODUCTS
            )
            # Insert Customers
            conn.executemany(
                "INSERT INTO customers (customer_id, name, email, tier, created_at) VALUES (?, ?, ?, ?, ?);",
                CUSTOMERS
            )
            # Insert Sales
            conn.executemany(
                "INSERT INTO sales (order_id, customer_id, product_id, quantity, unit_price, total_amount, status, order_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
                SALES
            )
            # Insert Returns
            conn.executemany(
                "INSERT INTO returns (return_id, order_id, product_id, customer_id, reason, status, return_date, refund_amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
                RETURNS
            )
        print(f"[+] Successfully seeded {len(PRODUCTS)} products, {len(CUSTOMERS)} customers, {len(SALES)} orders, and {len(RETURNS)} returns.")
    finally:
        conn.close()

if __name__ == "__main__":
    seed_database()
