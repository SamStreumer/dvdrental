import duckdb

con = duckdb.connect("/Users/samstreumer/Documents/SchoolFolder/dvdrental/dvdrental/dvdrental.duckdb")

print("=== ALLE TABELLEN IN DATABASE 1 (waar DBT werkt) ===")
all_tables = con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main' ORDER BY table_name").fetchall()

for table in all_tables:
    print(f"- {table[0]}")
    
# Check ook of er tabellen zijn die beginnen met bepaalde prefixes
print("\n=== CHECK VOOR DBT PREFIXES ===")
for prefix in ['dim', 'fct', 'main_', 'dbt_']:
    tables = con.execute(f"SELECT table_name FROM information_schema.tables WHERE table_name LIKE '{prefix}%'").fetchall()
    if tables:
        print(f"\nTabellen die beginnen met '{prefix}':")
        for t in tables:
            print(f"  - {t[0]}")

con.close()