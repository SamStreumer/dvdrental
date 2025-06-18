# Maak /dvdrental/which_db.py
import duckdb

print("=== DATABASE 1: /dvdrental/dvdrental/dvdrental.duckdb ===")
con1 = duckdb.connect("/Users/samstreumer/Documents/SchoolFolder/dvdrental/dvdrental/dvdrental.duckdb")
tables1 = con1.execute("SHOW TABLES").fetchall()
print(f"Aantal tabellen: {len(tables1)}")
for t in tables1:
    print(f"- {t[0]}")
con1.close()

print("\n=== DATABASE 2: /dvdrental/dvdrental.duckdb ===")
con2 = duckdb.connect("/Users/samstreumer/Documents/SchoolFolder/dvdrental/dvdrental.duckdb")
tables2 = con2.execute("SHOW TABLES").fetchall()
print(f"Aantal tabellen: {len(tables2)}")
for t in tables2:
    print(f"- {t[0]}")
con2.close()