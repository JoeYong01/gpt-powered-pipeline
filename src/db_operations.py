import sqlite3


def execute_query(query: str) -> None:
    """executes a sqllite query"""
    con = sqlite3.connect("db/gpt-powered-pipeline.db")
    cur = con.cursor()
    cur.execute(query)
    if query.strip().upper().startswith("SELECT"):
        result = cur.fetchall()
        return result
    else:
        con.commit()
    cur.close()
    con.close()

def insert_into_database(respondant_id, agent_id, is_resolved, feature_columns, call_logs, timestamp) -> None:
    """executes a sqllite query"""
    con = sqlite3.connect("db/gpt-powered-pipeline.db")
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO call_logs(respondant_id, agent_id, is_resolved, feature_columns, call_logs, timestamp)
        VALUES(?, ?, ?, ?, ?, ?)
        """,
        (respondant_id, agent_id, is_resolved, feature_columns, call_logs, timestamp)
    )
    con.commit()
    cur.close()
    con.close()

