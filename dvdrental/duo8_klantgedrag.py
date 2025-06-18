import duckdb
import matplotlib.pyplot as plt
import seaborn as sns

# Verbind met DuckDB - gebruik de juiste database
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
        pc.LocationKey,
        pc.Amount_AVG,
        dl.CityCountry
    FROM main_main_fct.payment_city pc
    JOIN main_main_dim.dim_location dl ON pc.LocationKey = dl.LocationKey
    ORDER BY pc.Amount_AVG DESC
    LIMIT 5
""").fetchdf()

for idx, row in steden_data.iterrows():
    print(f"  {idx+1}. {row['CityCountry']}: €{row['Amount_AVG']:.2f}")

# Visualisaties
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Duo 8: Klantgedrag Analyse', fontsize=16)

# 1. Histogram van klantopbrengsten
opbrengst_data = con.execute("SELECT Amount_SUM FROM main_main_dim.payment_customer").fetchdf()
axes[0, 0].hist(opbrengst_data['Amount_SUM'], bins=30, edgecolor='black', alpha=0.7)
axes[0, 0].axvline(100, color='red', linestyle='--', linewidth=2, label='€100 grens')
axes[0, 0].set_title('Verdeling van Totale Opbrengst per Klant')
axes[0, 0].set_xlabel('Totale Opbrengst (€)')
axes[0, 0].set_ylabel('Aantal Klanten')
axes[0, 0].legend()

# 2. Top 10 beste klanten
top_klanten = con.execute("""
    SELECT 
        dc.FullName,
        pc.Amount_SUM
    FROM main_main_dim.payment_customer pc
    JOIN main_main_dim.Dim_Customer dc ON pc.CustomerKey = dc.CustomerKey
    ORDER BY pc.Amount_SUM DESC
    LIMIT 10
""").fetchdf()

axes[0, 1].barh(top_klanten['FullName'], top_klanten['Amount_SUM'], color='green')
axes[0, 1].set_title('Top 10 Beste Klanten')
axes[0, 1].set_xlabel('Totale Opbrengst (€)')
axes[0, 1].invert_yaxis()

# 3. Gemiddelde opbrengst per stad
stad_plot = con.execute("""
    SELECT 
        dl.CityCountry,
        pc.Amount_AVG
    FROM main_main_fct.payment_city pc
    JOIN main_main_dim.dim_location dl ON pc.LocationKey = dl.LocationKey
    ORDER BY pc.Amount_AVG DESC
    LIMIT 15
""").fetchdf()

axes[1, 0].bar(range(len(stad_plot)), stad_plot['Amount_AVG'], color='skyblue')
axes[1, 0].set_xticks(range(len(stad_plot)))
axes[1, 0].set_xticklabels(stad_plot['CityCountry'], rotation=45, ha='right')
axes[1, 0].set_title('Top 15 Steden - Gemiddelde Opbrengst')
axes[1, 0].set_ylabel('Gemiddelde Opbrengst (€)')

# 4. Klanten per opbrengst categorie
categories = con.execute("""
    SELECT 
        CASE 
            WHEN Amount_SUM < 50 THEN '< €50'
            WHEN Amount_SUM < 100 THEN '€50-100'
            WHEN Amount_SUM < 150 THEN '€100-150'
            ELSE '> €150'
        END as categorie,
        COUNT(*) as aantal
    FROM main_main_dim.payment_customer
    GROUP BY categorie
    ORDER BY 
        CASE categorie
            WHEN '< €50' THEN 1
            WHEN '€50-100' THEN 2
            WHEN '€100-150' THEN 3
            ELSE 4
        END
""").fetchdf()

axes[1, 1].pie(categories['aantal'], labels=categories['categorie'], autopct='%1.1f%%')
axes[1, 1].set_title('Klanten per Opbrengst Categorie')

plt.tight_layout()
plt.savefig('/Users/samstreumer/Documents/SchoolFolder/dvdrental/dvdrental/analyses/duo8_visualisaties.png', dpi=300)
plt.show()

con.close()

print("\n✅ Analyse compleet! Visualisaties opgeslagen als 'duo8_visualisaties.png'")