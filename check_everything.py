import duckdb

con = duckdb.connect("/Users/samstreumer/Documents/SchoolFolder/dvdrental/dvdrental/dvdrental.duckdb")

print("=== ALLE OBJECTEN MET SHOW ALL TABLES ===")
all_objects = con.execute("SHOW ALL TABLES").fetchall()
print(f"Totaal aantal objecten: {len(all_objects)}")

for obj in all_objects:
    # obj[2] is de naam, obj[1] is het schema
    print(f"- {obj[1]}.{obj[2]}")

# Probeer de star schema tabellen direct
print("\n=== DIRECTE CHECKS ===")
star_tables = ['Dim_Customer', 'dim_location', 'payment_customer', 'payment_city']
for table in star_tables:
    try:
        count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"✅ {table}: {count} rows")
    except Exception as e:
        print(f"❌ {table}: niet gevonden")

con.close()