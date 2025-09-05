import pandas as pd
import matplotlib.pyplot as plt

# Datenquellen:
# Ameco: CPI, national (ZCPIN);  
# Ameco: GDP per head, at current prices (HVGDP)
# Ameco: Total population (national accounts) (NPTD)
# BMAS: https://www.bmas.de/DE/Service/Publikationen/Broschueren/a230-25-sozialbudget-2024.html , bzw. 
# https://www.bmas.de/SharedDocs/Downloads/DE/Publikationen/Sozialbudget/sozialleistungen-insgesamt-1960-2024.csv?__blob=publicationFile&v=1


# --- Hardcoded Data ---

# Sozialleistungen in Milliarden Euro
sozialleistungen_data = {
    1991: 394.9, 1992: 448.3, 1993: 472.9, 1994: 495.5, 1995: 522.7, 1996: 552.5,
    1997: 556.1, 1998: 569.5, 1999: 590.7, 2000: 607.4, 2001: 624.9, 2002: 648.1,
    2003: 660.9, 2004: 659.3, 2005: 664.4, 2006: 663.5, 2007: 673.2, 2008: 695.3,
    2009: 752.5, 2010: 770.2, 2011: 774.9, 2012: 794.2, 2013: 822.9, 2014: 854.8,
    2015: 892.4, 2016: 932.9, 2017: 968.0, 2018: 1001.0, 2019: 1047.4, 2020: 1121.8,
    2021: 1161.5, 2022: 1192.6, 2023: 1262.2, 2024: 1345.4
}

# Verbraucherpreisindex (CPI), Basisjahr 2020 = 100
cpi_data = {
    1991: 62.1, 1992: 65.3, 1993: 68.2, 1994: 70.0, 1995: 71.2, 1996: 72.2, 1997: 73.6,
    1998: 74.3, 1999: 74.8, 2000: 75.8, 2001: 77.3, 2002: 78.4, 2003: 79.2, 2004: 80.6,
    2005: 81.8, 2006: 83.1, 2007: 85.0, 2008: 87.2, 2009: 87.5, 2010: 88.5, 2011: 90.3,
    2012: 92.1, 2013: 93.5, 2014: 94.4, 2015: 94.9, 2016: 95.3, 2017: 96.8, 2018: 98.4,
    2019: 99.9, 2020: 100.0, 2021: 103.1, 2022: 110.2, 2023: 116.7, 2024: 119.3
}


# Bevölkerungsdaten für Deutschland (in Millionen)
population_data = {
    1991: 79.973, 1992: 80.500, 1993: 80.946, 1994: 81.147, 1995: 81.308,
    1996: 81.466, 1997: 81.510, 1998: 81.446, 1999: 81.422, 2000: 81.457,
    2001: 81.517, 2002: 81.517, 2003: 81.549, 2004: 81.456, 2005: 81.337,
    2006: 81.173, 2007: 80.992, 2008: 80.864, 2009: 80.483, 2010: 80.284,
    2011: 80.275, 2012: 80.426, 2013: 80.426, 2014: 80.983, 2015: 81.687,
    2016: 82.657, 2017: 82.657, 2018: 82.906, 2019: 83.093, 2020: 83.161,
    2021: 83.196, 2022: 83.798, 2023: 84.514, 2024: 84.717
}

# BIP pro Kopf preisbereinigt (in 1000 €)
domesticproduct_per_capita = {
    1991: 30.4, 1992: 30.8, 1993: 30.4, 1994: 31.1, 1995: 31.5,
    1996: 31.7, 1997: 32.3, 1998: 33.0, 1999: 33.7, 2000: 34.7,
    2001: 35.2, 2002: 35.1, 2003: 34.9, 2004: 35.4, 2005: 35.7,
    2006: 37.2, 2007: 38.4, 2008: 38.8, 2009: 36.8, 2010: 38.4,
    2011: 39.9, 2012: 40.0, 2013: 40.0, 2014: 40.7, 2015: 41.0,
    2016: 41.6, 2017: 42.6, 2018: 43.0, 2019: 43.3, 2020: 41.5,
    2021: 43.0, 2022: 43.3, 2023: 42.8, 2024: 42.6
}


# --- Datenverarbeitung ---

# Erstellen von DataFrames aus den Dictionaries
sozialleistungen_df = pd.DataFrame(list(sozialleistungen_data.items()), columns=['Year', 'Sozialleistungen_Mrd_EUR'])
cpi_df = pd.DataFrame(list(cpi_data.items()), columns=['Year', 'CPI'])
population_df = pd.DataFrame(list(population_data.items()), columns=['Year', 'Population_Mio'])
gdp_df = pd.DataFrame(list(domesticproduct_per_capita.items()), columns=['Year', 'GDP_pro_Kopf_real_Tsd_EUR'])

# Zusammenführen der DataFrames
df = pd.merge(sozialleistungen_df, cpi_df, on='Year')
df = pd.merge(df, population_df, on='Year')
df = pd.merge(df, gdp_df, on='Year')

# --- Berechnungen ---

# 1. Berechnung und Indexierung der Sozialleistungen pro Kopf
df['Sozialleistungen_pro_Kopf'] = (df['Sozialleistungen_Mrd_EUR'] * 1e9) / (df['Population_Mio'] * 1e6)
cpi_2015 = df.loc[df['Year'] == 2015, 'CPI'].iloc[0]
df['CPI_2015_100'] = df['CPI'] / cpi_2015 * 100
df['Sozialleistungen_pro_Kopf_real'] = (df['Sozialleistungen_pro_Kopf'] / df['CPI_2015_100']) * 100
index_sozial_2015 = df.loc[df['Year'] == 2015, 'Sozialleistungen_pro_Kopf_real'].iloc[0]
df['Sozialleistungen_pro_Kopf_indexed'] = (df['Sozialleistungen_pro_Kopf_real'] / index_sozial_2015) * 100

# 2. Indexierung des realen BIP pro Kopf (ist bereits real und pro Kopf)
gdp_pc_2015 = df.loc[df['Year'] == 2015, 'GDP_pro_Kopf_real_Tsd_EUR'].iloc[0]
df['GDP_pro_Kopf_indexed'] = (df['GDP_pro_Kopf_real_Tsd_EUR'] / gdp_pc_2015) * 100


# --- Erstellen des Plots ---

plt.figure(figsize=(12, 8))
plt.plot(df['Year'], df['Sozialleistungen_pro_Kopf_indexed'], marker='o', linestyle='-', label='Reale Sozialleistungen p.K.')
plt.plot(df['Year'], df['GDP_pro_Kopf_indexed'], marker='s', linestyle='--', label='Reales BIP p.K.')

plt.title('Reale Entwicklung: Sozialleistungen vs. BIP pro Kopf (Index 2015=100)')
plt.xlabel('Jahr')
plt.ylabel('Index (2015=100)')
plt.axhline(y=100, color='gray', linestyle=':', linewidth=1) # Fügt Referenzlinie für Index 100 hinzu
plt.legend() # Zeigt die Legende an
plt.grid(True)
plt.tight_layout()

# Grafik speichern
plt.savefig('sozialleistungen_vs_bip_final.png')

print("Die kombinierte Grafik wurde erfolgreich als 'sozialleistungen_vs_bip_final.png' gespeichert.")

plt.show()