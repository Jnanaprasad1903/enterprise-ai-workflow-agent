-- ==========================================================
-- Enterprise AI Workflow Agent: Database Schema (SQLite)
-- ==========================================================

-- Products Table
CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL,
    warranty_months INTEGER NOT NULL
);

-- Customers Table
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    tier TEXT NOT NULL DEFAULT 'Standard', -- 'VIP', 'Standard'
    created_at TEXT NOT NULL
);

-- Sales / Orders Table
CREATE TABLE IF NOT EXISTS sales (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    total_amount REAL NOT NULL,
    status TEXT NOT NULL, -- 'Completed', 'Returned', 'Processing'
    order_date TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Returns Table
CREATE TABLE IF NOT EXISTS returns (
    return_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    reason TEXT NOT NULL,
    status TEXT NOT NULL, -- 'Refunded', 'Pending', 'Rejected'
    return_date TEXT NOT NULL,
    refund_amount REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES sales(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Indexes for Query Performance & Analytical Aggregations
CREATE INDEX IF NOT EXISTS idx_sales_product_id ON sales(product_id);
CREATE INDEX IF NOT EXISTS idx_sales_order_date ON sales(order_date);
CREATE INDEX IF NOT EXISTS idx_returns_product_id ON returns(product_id);
CREATE INDEX IF NOT EXISTS idx_returns_order_id ON returns(order_id);
