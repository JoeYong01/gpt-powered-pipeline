"""creates a sqlite db for demonstration purposes"""
import sqlite3


def execute_query(query: str) -> None:
    """executes a sqllite query"""
    con = sqlite3.connect("db/gpt-powered-pipeline.db")
    cur = con.cursor()
    cur.execute(query)
    con.commit()


QUERY = """
CREATE TABLE call_logs(
    id INTEGER PRIMARY KEY,
    respondant_id INTEGER DEFAULT NULL,
    caller_id INTEGER DEFAULT NULL,
    is_resolved INTEGER DEFAULT NULL,
    feature_columns INTEGER DEFAULT NULL,
    call_logs TEXT DEFAULT NULL,
    timestamp TEXT
);
"""

execute_query(QUERY)
