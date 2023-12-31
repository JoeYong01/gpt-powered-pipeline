import logging
import sqlite3


logger = logging.getLogger("db_operations.py")

def execute_query(query: str) -> None:
    """executes a sqllite query"""
    try:
        logger.info("running function: execute_query.")
        con = sqlite3.connect("db/gpt-powered-pipeline.db")
        cur = con.cursor()
        cur.execute(query)
        if query.strip().upper().startswith("SELECT"):
            logger.debug("detected a SELECT statment.")
            result = cur.fetchall()
            return result
        else:
            logger.debug("detected a DML/DDL statement.")
            con.commit()
    except sqlite3.Error as e:
        logger.exception("sqlite3 Exception in execute_query: %s", e)
    except Exception as e:
        logger.exception("Exception in execute_query: %s", e)
    finally:
        cur.close()
        con.close()
        logger.debug("connection is closed.")


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
        logger.info("running function: insert_into_database.")
        con = sqlite3.connect("db/gpt-powered-pipeline.db")
        cur = con.cursor()
        cur.execute(
            query,
            (respondant_id, agent_id, is_resolved, feature_columns, call_logs, timestamp)
        )
        con.commit()
        logger.debug("Executed query: %s", query)
    except sqlite3.Error as e:
        logger.exception("sqlite3 Exception in insert_into_database : %s", e)
    except Exception as e:
        logger.exception("Exception in insert_into_database: %s", e)
    finally:
        cur.close()
        con.close()
        logger.debug("database connection is closed.")
