import duckdb

con = duckdb.connect("/Users/samstreumer/Documents/SchoolFolder/dvdrental/dvdrental/dvdrental.duckdb")

print("=== ALLE TABELLEN MET SCHEMA ===")
result = con.execute("""
    SELECT table_schema, table_name 
    FROM information_schema.tables 
    WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
    ORDER BY table_schema, table_name
""").fetchall()

for schema, table in result:
    print(f"{schema}.{table}")

con.close()