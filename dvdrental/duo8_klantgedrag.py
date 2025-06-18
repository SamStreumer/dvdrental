import duckdb
import matplotlib.pyplot as plt
import seaborn as sns

# Verbind met DuckDB
con = duckdb.connect("/Users/samstreumer/Documents/SchoolFolder/dvdrental/dvdrental/dvdrental.duckdb")

print("=== DUO 8: KLANTGEDRAG ANALYSE ===\n")

# Vraag 1: Wat is de gemiddelde opbrengst per klant?
print("VRAAG 1: Gemiddelde opbrengst per klant")
result_vraag1 = con.execute("""
    SELECT 
        AVG(Amount_SUM) as gem_totale_opbrengst_per_klant,
        AVG(Amount_AVG) as gem_opbrengst_per_transactie,
        COUNT(*) as aantal_klanten
    FROM main_main_dim.payment_customer
""").fetchone()

gemiddelde_opbrengst = result_vraag1[0]
gemiddelde_per_transactie = result_vraag1[1]
aantal_klanten = result_vraag1[2]

print(f"- Gemiddelde totale opbrengst per klant: €{gemiddelde_opbrengst:.2f}")
print(f"- Gemiddelde opbrengst per transactie: €{gemiddelde_per_transactie:.2f}")
print(f"- Totaal aantal klanten: {aantal_klanten}")

# Vraag 2: Hoeveel klanten hebben meer dan €100 uitgegeven?
print("\nVRAAG 2: Klanten met meer dan €100 opbrengst")
result_vraag2 = con.execute("""
    SELECT 
        COUNT(*) as aantal_klanten_100plus,
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM main_main_dim.payment_customer) as percentage
    FROM main_main_dim.payment_customer
    WHERE Amount_SUM > 100
""").fetchone()

aantal_boven_100 = result_vraag2[0]
percentage_boven_100 = result_vraag2[1]

print(f"- Aantal klanten met >€100: {aantal_boven_100}")
print(f"- Percentage van totaal: {percentage_boven_100:.1f}%")

# Vraag 3: Wat is de gemiddelde opbrengst per stad?
print("\nVRAAG 3: Gemiddelde opbrengst per stad (Top 10)")
steden_data = con.execute("""
    SELECT 
        pc.LocationKey,
        pc.Amount_AVG,
        dl.CityCountry
    FROM main_main_fct.payment_city pc
    JOIN main_main_dim.dim_location dl ON pc.LocationKey = dl.LocationKey
    ORDER BY pc.Amount_AVG DESC
    LIMIT 10
""").fetchdf()

for idx, row in steden_data.iterrows():
    print(f"  {idx+1}. {row['CityCountry']}: €{row['Amount_AVG']:.2f}")

# Visualisaties voor de 3 vragen
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Duo 8: Klantgedrag Analyse - 3 Hoofdvragen', fontsize=16)

# Visualisatie Vraag 1: Gemiddelde opbrengst verdeling
opbrengst_data = con.execute("SELECT Amount_SUM FROM main_main_dim.payment_customer").fetchdf()
axes[0].hist(opbrengst_data['Amount_SUM'], bins=30, edgecolor='black', alpha=0.7)
axes[0].axvline(gemiddelde_opbrengst, color='red', linestyle='--', linewidth=2, label=f'Gemiddelde: €{gemiddelde_opbrengst:.2f}')
axes[0].set_title('Vraag 1: Verdeling Klantopbrengsten')
axes[0].set_xlabel('Totale Opbrengst per Klant (€)')
axes[0].set_ylabel('Aantal Klanten')
axes[0].legend()

# Visualisatie Vraag 2: Klanten boven/onder €100
onder_100 = aantal_klanten - aantal_boven_100
axes[1].bar(['≤ €100', '> €100'], [onder_100, aantal_boven_100], color=['lightcoral', 'lightgreen'])
axes[1].set_title('Vraag 2: Klanten per Opbrengst Categorie')
axes[1].set_ylabel('Aantal Klanten')
for i, v in enumerate([onder_100, aantal_boven_100]):
    axes[1].text(i, v + 5, str(v), ha='center', fontweight='bold')

# Visualisatie Vraag 3: Top 10 steden
axes[2].barh(steden_data['CityCountry'], steden_data['Amount_AVG'], color='skyblue')
axes[2].set_title('Vraag 3: Top 10 Steden - Gemiddelde Opbrengst')
axes[2].set_xlabel('Gemiddelde Opbrengst (€)')
axes[2].invert_yaxis()

plt.tight_layout()
plt.savefig('/Users/samstreumer/Documents/SchoolFolder/dvdrental/dvdrental/analyses/duo8_3vragen.png', dpi=300)
plt.show()

con.close()

print("\nAnalyse compleet! Visualisaties opgeslagen als 'duo8_3vragen.png'")