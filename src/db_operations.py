import psycopg2


PG_DB_PARAMS = {
    "host": "",
    "user": "",
    "password": "",
    "database": ""
}


def execute_query(query: str) -> None:
    """Takes a query as an input & executes it against a postgres database"""
    try:
        with psycopg2.connect(**PG_DB_PARAMS) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
    except psycopg2.errors as e:
        print(f"a psycopg2 error occured: {e}")
    except Exception as e:
        print(f"an error occured: {e}")
