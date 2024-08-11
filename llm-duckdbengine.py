from sqlalchemy import create_engine
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine

engine = create_engine("duckdb:///mobile.duckdb")


def init(conn):
    conn.exec_driver_sql("""
        CREATE TABLE IF NOT EXISTS MOBILE AS 
        SELECT * FROM read_csv('data/mobile/mobile-price-data.csv');
    """)


def test_query(conn):
    cursor = conn.exec_driver_sql("SELECT * FROM MOBILE LIMIT 3;")
    print(cursor.fetchall())


def create_test(eng):
    with eng.connect() as connection:
        init(connection)
        test_query(connection)


if __name__ == '__main__':
    create_test(engine)
    sql_db = SQLDatabase(engine, include_tables=["mobile"])
    query_engine = NLSQLTableQueryEngine(sql_database=sql_db)

    response = query_engine.query("What is the phone with best overall features?")
    print(response.response)
