import pandas as pd
import matplotlib.pyplot as plt
import json

# Charger le fichier CSV de production
df = pd.read_csv("./data_csv/consumption_zones.csv")

# Convertir la colonne 'datetime' en type datetime
df["datetime"] = pd.to_datetime(df["datetime"], format="%Y-%m-%d %H:%M:%S")

# Ne conserver que la zone "France Métropolitaine"
df = df[df["zone"] == "France Métropolitaine"]

# Demander à l'utilisateur la plage horaire
start_str = input("Entrez la date et l'heure de début (YYYY-MM-DD HH:MM:SS) : ")
end_str = input("Entrez la date et l'heure de fin (YYYY-MM-DD HH:MM:SS) : ")

try:
    start_dt = pd.to_datetime(start_str, format="%Y-%m-%d %H:%M:%S")
    end_dt = pd.to_datetime(end_str, format="%Y-%m-%d %H:%M:%S")
except Exception as e:
    print("Erreur de format de date :", e)
    exit(1)

# Filtrer les enregistrements dans la plage demandée et trier par date
filtered = df[(df["datetime"] >= start_dt) & (df["datetime"] <= end_dt)]
filtered = filtered.sort_values(by="datetime")

if filtered.empty:
    print("Aucune donnée trouvée dans cette plage horaire.")
    exit(0)

# Extraire la liste des types de production à partir de la première ligne (si disponible)
try:
    sample_row = filtered.iloc[0]
    prod_dict = json.loads(sample_row["power_Production_Breakdown"])
    production_types = list(prod_dict.keys())
except Exception as e:
    print("Erreur lors du parsing de la première ligne :", e)
    exit(1)

# Préparer un dictionnaire pour construire le DataFrame des séries temporelles
data_dict = {"datetime": []}
for p_type in production_types:
    data_dict[p_type] = []

# Remplir le dictionnaire pour chaque enregistrement
for index, row in filtered.iterrows():
    dt = row["datetime"]
    try:
        prod = json.loads(row["power_Production_Breakdown"])
    except Exception as e:
        print(f"Erreur de parsing JSON à la date {dt}: {e}")
        continue
    data_dict["datetime"].append(dt)
    for p_type in production_types:
        val = prod.get(p_type, 0)
        if val is None:
            val = 0
        data_dict[p_type].append(val)

# Créer un DataFrame avec les données
df_prod = pd.DataFrame(data_dict)

# Tracer le graphique
plt.figure(figsize=(12, 8))
for p_type in production_types:
    plt.plot(df_prod["datetime"], df_prod[p_type], marker='o', label=p_type)

plt.xlabel("Date et Heure")
plt.ylabel("Production (en kWh)")  # Modifier l'unité si nécessaire
plt.title("Évolution de la production d'énergie par type en France")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
