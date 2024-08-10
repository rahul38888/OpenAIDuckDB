import duckdb

con = duckdb.connect("datacamp.duckdb")

if __name__ == '__main__':
    con.execute("""
        CREATE TABLE IF NOT EXISTS EXERCISE AS 
        SELECT * FROM read_csv('data/gym_exercise_dataset.csv')
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS STRETCH AS 
        SELECT * FROM read_csv('data/stretch_exercise_dataset.csv')
    """)
    # con.execute("SHOW ALL TABLES").fetchdf()

    rel = con.table("EXERCISE")
    print(rel.columns)

    rel = con.table("STRETCH")
    print(rel.columns)

    res = con.query("""
        SELECT * FROM STRETCH LIMIT 2
    """)

    print(res.df())

