import logging
import sqlite3


def execute_query(query: str) -> None:
    """executes a sqllite query"""
    try:
        logging.info("running execute_query.")
        con = sqlite3.connect("db/gpt-powered-pipeline.db")
        cur = con.cursor()
        cur.execute(query)
        if query.strip().upper().startswith("SELECT"):
            logging.debug("detected a SELECT statment.")
            result = cur.fetchall()
            return result
        else:
            logging.debug("detected a DML/DDL statement.")
            con.commit()
    except sqlite3.Error as e:
        logging.exception("sqlite3 Exception in execute_query: %s", e)
    except Exception as e:
        logging.exception("Exception in execute_query: %s", e)
    finally:
        cur.close()
        con.close()
        logging.debug("connection is closed.")


def insert_into_database(
    respondant_id,
    agent_id,
    is_resolved,
    feature_columns,
    call_logs,
    timestamp
) -> None:
    """executes a sqllite query"""
    query = """
    INSERT INTO call_logs(respondant_id, agent_id, is_resolved, feature_columns, call_logs, timestamp)
    VALUES(?, ?, ?, ?, ?, ?)
    """
    try:
        logging.info("running function: insert_into_database.")
        con = sqlite3.connect("db/gpt-powered-pipeline.db")
        cur = con.cursor()
        cur.execute(
            query,
            (respondant_id, agent_id, is_resolved, feature_columns, call_logs, timestamp)
        )
        con.commit()
        logging.debug("Executed query: %s", query)
    except sqlite3.Error as e:
        logging.exception("sqlite3 Exception in insert_into_database : %s", e)
    except Exception as e:
        logging.exception("Exception in insert_into_database: %s", e)
    finally:
        cur.close()
        con.close()
        logging.debug("database connection is closed.")
