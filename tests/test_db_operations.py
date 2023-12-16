"""runs test against db_operations source code"""
import os
from datetime import datetime
from random import randint
from src.db_operations import(
    execute_query,
    insert_into_database
)

random_int = randint(1, 1000)
datetime_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
test_insert_into_database_query = f"""
SELECT * FROM call_logs WHERE timestamp = '{datetime_now}'
"""

def test_execute_query_create_read_update() -> None:
    """tests against Create, Read, Update operations"""
    execute_query(f"CREATE TABLE IF NOT EXISTS test_{random_int} AS SELECT 1 AS col_1")
    execute_query(f"UPDATE test_{random_int} SET col_1 = 2 WHERE col_1 = 1")
    result = execute_query(f"SELECT col_1 FROM test_{random_int}")
    assert result == [(2,)]


def test_execute_query_delete() -> None:
    """tests against Delete operations"""
    execute_query(f"DELETE FROM test_{random_int} WHERE col_1 = 2")
    result = execute_query(f"SELECT col_1 FROM test_{random_int}")
    assert result == []


def test_insert_into_database() -> None:
    """tests against the specialized function for inserting"""
    insert_into_database(
        respondant_id = 1,
        agent_id = 1,
        is_resolved = 1,
        feature_columns = 1,
        call_logs = 'test',
        timestamp = datetime_now
    )
    result = execute_query(test_insert_into_database_query)
    assert result == [(1, 1, 1, 1, 'test', datetime_now)]
