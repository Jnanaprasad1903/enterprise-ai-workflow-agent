import json
from typing import Dict, Any, List, Optional
from src.database.db import execute_read_query, get_table_schema

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False

def format_rows_as_markdown(rows: List[Dict[str, Any]]) -> str:
    """Formats a list of row dictionaries into a markdown table for LLM consumption."""
    if not rows:
        return "Query returned 0 rows."
    
    headers = list(rows[0].keys())
    data = [[row.get(h, "") for h in headers] for row in rows]
    
    if HAS_TABULATE:
        return tabulate(data, headers=headers, tablefmt="github")
    
    # Manual Markdown table fallback if tabulate isn't loaded yet
    header_line = "| " + " | ".join(headers) + " |"
    sep_line = "| " + " | ".join(["---"] * len(headers)) + " |"
    data_lines = [
        "| " + " | ".join(str(val) for val in row_vals) + " |"
        for row_vals in data
    ]
    return "\n".join([header_line, sep_line] + data_lines)

def query_database(sql_query: str) -> str:
    """
    Executes a read-only SQL query against the enterprise SQLite database.
    Use this tool whenever you need structured business data such as:
    - Products, categories, prices, stock levels
    - Sales numbers, order histories, revenue metrics
    - Return counts, return reasons, and refund totals
    
    Args:
        sql_query: A valid SQLite SELECT statement (e.g., 'SELECT name, SUM(quantity) FROM sales ...')
        
    Returns:
        A Markdown-formatted table containing the query results or an error explanation.
    """
    try:
        # Strip trailing semicolons and whitespace
        clean_sql = sql_query.strip().rstrip(";")
        rows = execute_read_query(clean_sql)
        formatted_table = format_rows_as_markdown(rows)
        return (
            f"Query Executed:\n```sql\n{clean_sql}\n```\n\n"
            f"Results ({len(rows)} rows):\n{formatted_table}"
        )
    except Exception as e:
        return f"Database Error: {str(e)}\nPlease check table names and column definitions using describe_database()."

def describe_database() -> str:
    """
    Returns the complete schema of the enterprise database, including table names,
    columns, constraints, and relationships.
    Call this if you are unsure which tables or columns to query.
    """
    try:
        schema = get_table_schema()
        return f"Enterprise Database Schema:\n```sql\n{schema}\n```"
    except Exception as e:
        return f"Error retrieving schema: {str(e)}"
