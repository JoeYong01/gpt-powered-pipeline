"""creates a sqlite db for demonstration purposes"""
import sqlite3


def execute_query(query: str) -> None:
    """executes a sqllite query"""
    con = sqlite3.connect("db/gpt-powered-pipeline.db")
    cur = con.cursor()
    cur.execute(query)
    return cur.fetchall


QUERY = """
SELECT * FROM call_logs;
"""

print(execute_query(QUERY))
