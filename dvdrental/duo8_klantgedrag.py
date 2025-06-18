import duckdb
import matplotlib.pyplot as plt
import seaborn as sns

# Verbind met de EXACTE database locatie
con = duckdb.connect("/Users/samstreumer/Documents/SchoolFolder/dvdrental/dvdrental/dvdrental.duckdb")

print("=== DUO 8: KLANTGEDRAG ANALYSE ===\n")

# Vraag 1: Wat is de gemiddelde opbrengst per klant?
print("VRAAG 1: Gemiddelde opbrengst per klant")
result = con.execute("""
    SELECT 
        AVG(Amount_SUM) as gem_totale_opbrengst_per_klant,
        AVG(Amount_AVG) as gem_opbrengst_per_transactie,
        COUNT(*) as aantal_klanten
    FROM main_main_dim.payment_customer
""").fetchone()

print(f"- Gemiddelde totale opbrengst per klant: €{result[0]:.2f}")
print(f"- Gemiddelde opbrengst per transactie: €{result[1]:.2f}")
print(f"- Totaal aantal klanten: {result[2]}")

# Vraag 2: Hoeveel klanten hebben meer dan €100 uitgegeven?
print("\nVRAAG 2: Klanten met meer dan €100 opbrengst")
result = con.execute("""
    SELECT 
        COUNT(*) as aantal_klanten_100plus,
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM main_main_dim.payment_customer) as percentage
    FROM main_main_dim.payment_customer
    WHERE Amount_SUM > 100
""").fetchone()

print(f"- Aantal klanten met >€100: {result[0]}")
print(f"- Percentage van totaal: {result[1]:.1f}%")

# Vraag 3: Wat is de gemiddelde opbrengst per stad?
print("\nVRAAG 3: Gemiddelde opbrengst per stad (Top 5)")
steden_data = con.execute("""
    SELECT 
        LocationKey,
        Amount_AVG
    FROM main_main_fct.payment_city
    ORDER BY Amount_AVG DESC
    LIMIT 5
""").fetchdf()

for idx, row in steden_data.iterrows():
    print(f"  {idx+1}. Stad ID {row['LocationKey']}: €{row['Amount_AVG']:.2f}")

con.close()