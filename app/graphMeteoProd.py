import pandas as pd
import matplotlib.pyplot as plt
import json

# Charger les fichiers CSV
df_carbon = pd.read_csv("./data_csv/aggregated_data.csv")
df_production = pd.read_csv("./data_csv/consumption_zones.csv")

# Convertir et nettoyer les dates
df_carbon["date_time"] = pd.to_datetime(df_carbon["date_time"], format="%Y-%m-%d %H:%M:%S").apply(lambda dt: dt.replace(second=0))
df_production["datetime"] = pd.to_datetime(df_production["datetime"], format="%Y-%m-%d %H:%M:%S")

# Filtrer la zone France Métropolitaine
df_production = df_production[df_production["zone"] == "France Métropolitaine"]

# Demander la plage horaire
start_str = input("Entrez la date et l'heure de début (YYYY-MM-DD HH:MM:SS) : ")
end_str = input("Entrez la date et l'heure de fin (YYYY-MM-DD HH:MM:SS) : ")

try:
    start_dt = pd.to_datetime(start_str)
    end_dt = pd.to_datetime(end_str)
except Exception as e:
    print("Erreur de format de date :", e)
    exit(1)

# Filtrer les données
filtered_carbon = df_carbon[(df_carbon["date_time"] >= start_dt) & (df_carbon["date_time"] <= end_dt)].drop_duplicates().sort_values("date_time")
filtered_production = df_production[(df_production["datetime"] >= start_dt) & (df_production["datetime"] <= end_dt)].sort_values("datetime")

if filtered_carbon.empty or filtered_production.empty:
    print("Aucune donnée trouvée dans cette plage horaire.")
    exit(0)

filtered_carbon["carbon_intensity_hWh"] = filtered_carbon["carbon_intensity"] * 1.0

try:
    sample_row = filtered_production.iloc[0]
    prod_dict = json.loads(sample_row["power_Production_Breakdown"])
    production_types = list(prod_dict.keys())
except Exception as e:
    print("Erreur lors du parsing de la première ligne :", e)
    exit(1)

data_dict = {"datetime": []}
for p_type in production_types:
    data_dict[p_type] = []

for index, row in filtered_production.iterrows():
    dt = row["datetime"]
    try:
        prod = json.loads(row["power_Production_Breakdown"])
    except Exception as e:
        print(f"Erreur de parsing JSON à la date {dt}: {e}")
        continue
    data_dict["datetime"].append(dt)
    for p_type in production_types:
        val = prod.get(p_type, 0) if prod.get(p_type) is not None else 0
        data_dict[p_type].append(val * 0.1)

df_prod = pd.DataFrame(data_dict)

fig, ax1 = plt.subplots(figsize=(14, 8))

# Tracer l'intensité carbonique
color = 'tomato'
ax1.set_xlabel("Date et Heure")
ax1.set_ylabel("Intensité Carbonique (gCO₂/hWh)", color=color)
ax1.plot(filtered_carbon["date_time"], filtered_carbon["carbon_intensity_hWh"], marker="o", color=color, label="Intensité Carbonique")
ax1.tick_params(axis='y', labelcolor=color)

# Créer un second axe pour la production
twin_ax = ax1.twinx()

for p_type in production_types:
    twin_ax.plot(df_prod["datetime"], df_prod[p_type], marker='o', label=p_type)
twin_ax.set_ylabel("Production (hWh)")
twin_ax.legend(loc='center left', bbox_to_anchor=(1.15, 0.5))

plt.title("Intensité Carbonique et Production d'Énergie en France")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()