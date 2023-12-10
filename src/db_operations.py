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
