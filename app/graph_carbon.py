import pandas as pd
import matplotlib.pyplot as plt

# Charger le fichier CSV
df = pd.read_csv("./data_csv/aggregated_data.csv")

# Convertir la colonne 'date_time' en type datetime
df["date_time"] = pd.to_datetime(df["date_time"], format="%Y-%m-%d %H:%M:%S")

# Remplacer les secondes par 00 en arrondissant à la minute
df["date_time"] = df["date_time"].apply(lambda dt: dt.replace(second=0))

# Supprimer les doublons (optionnellement, selon toutes les colonnes)
df = df.drop_duplicates()

# Demander à l'utilisateur la plage horaire
start_str = input("Entrez la date et l'heure de début (YYYY-MM-DD HH:MM:SS) : ")
end_str = input("Entrez la date et l'heure de fin (YYYY-MM-DD HH:MM:SS) : ")

try:
    start_dt = pd.to_datetime(start_str, format="%Y-%m-%d %H:%M:%S")
    end_dt = pd.to_datetime(end_str, format="%Y-%m-%d %H:%M:%S")
except Exception as e:
    print("Erreur de format de date :", e)
    exit(1)

# Filtrer les enregistrements dans la plage demandée
filtered = df[(df["date_time"] >= start_dt) & (df["date_time"] <= end_dt)]
filtered = filtered.sort_values(by="date_time")

if filtered.empty:
    print("Aucune donnée trouvée dans cette plage horaire.")
else:
    # Afficher les données filtrées dans la console
    print(filtered)

    # Tracer un graphique de l'évolution de l'intensité carbonique
    plt.figure(figsize=(10, 6))
    plt.plot(filtered["date_time"], filtered["carbon_intensity"], marker="o", linestyle="-", color="tomato")
    plt.xlabel("Date et Heure")
    plt.ylabel("Intensité Carbonique (gCO₂/kWh)")
    plt.title("Évolution de l'intensité carbonique en France")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
