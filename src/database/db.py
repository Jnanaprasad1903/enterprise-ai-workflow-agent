import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from src.config import DATABASE_PATH, BASE_DIR

SCHEMA_PATH = BASE_DIR / "src" / "database" / "schema.sql"

def get_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """Creates and returns a connection to the SQLite database with Row factory enabled."""
    target_path = db_path or DATABASE_PATH
    target_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(target_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db(db_path: Optional[Path] = None, schema_file: Optional[Path] = None) -> None:
    """Initializes the database using the schema.sql definition."""
    target_schema = schema_file or SCHEMA_PATH
    if not target_schema.exists():
        raise FileNotFoundError(f"Schema file not found at {target_schema}")
    
    with open(target_schema, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn = get_connection(db_path)
    try:
        with conn:
            conn.executescript(schema_sql)
    finally:
        conn.close()

def execute_read_query(query: str, params: Tuple = (), db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """
    Executes a SELECT query and returns the results as a list of dictionaries.
    Blocks dangerous write/drop operations for safety.
    """
    clean_query = query.strip()
    first_token = clean_query.split()[0].upper() if clean_query else ""
    
    if first_token not in ("SELECT", "WITH", "EXPLAIN", "PRAGMA"):
        raise ValueError(
            f"Security Violation: Read query tool only permits read-only statements (SELECT/WITH). "
            f"Encountered: {first_token}"
        )

    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def execute_write(query: str, params: Tuple = (), db_path: Optional[Path] = None) -> int:
    """Executes an INSERT/UPDATE/DELETE query within a transaction and returns rowcount."""
    conn = get_connection(db_path)
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.rowcount
    finally:
        conn.close()

def get_table_schema() -> str:
    """Returns a clean textual representation of the database schema for LLM context grounding."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
        )
        tables = cursor.fetchall()
        
        schema_text = []
        for table in tables:
            schema_text.append(f"-- Table: {table['name']}\n{table['sql']}\n")
        return "\n".join(schema_text)
    finally:
        conn.close()
