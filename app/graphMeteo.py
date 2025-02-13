import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Charger le fichier CSV
df = pd.read_csv("./data_csv/weather_data.csv")

# Convertir la colonne 'date_time' en type datetime
df["date_time"] = pd.to_datetime(df["date_time"], format="%Y-%m-%d %H:%M:%S")

# Demander à l'utilisateur la plage horaire
start_str = input("Entrez la date et l'heure de début (YYYY-MM-DD HH:MM:SS) : ")
end_str = input("Entrez la date et l'heure de fin (YYYY-MM-DD HH:MM:SS) : ")

try:
    start_dt = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
    end_dt = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
except Exception as e:
    print("Erreur de format de date :", e)
    exit(1)

# Filtrer le DataFrame selon la plage horaire
filtered = df[(df["date_time"] >= start_dt) & (df["date_time"] <= end_dt)]
filtered = filtered.sort_values(by="date_time")

if filtered.empty:
    print("Aucune donnée trouvée dans cette plage horaire.")
    exit(0)
else:
    print("Données filtrées :")
    print(filtered)

    # Créer un graphique avec 5 sous-graphes
    fig, axs = plt.subplots(5, 1, figsize=(12, 20), sharex=True)

    # Evolution de la température
    axs[0].plot(filtered["date_time"], filtered["temperature"], marker="o", linestyle="-", color="red")
    axs[0].set_ylabel("Température (°C)")
    axs[0].set_title("Évolution de la température")

    # Evolution de la couverture nuageuse
    axs[1].plot(filtered["date_time"], filtered["clouds"], marker="o", linestyle="-", color="blue")
    axs[1].set_ylabel("Couverture nuageuse (%)")
    axs[1].set_title("Évolution de la couverture nuageuse")

    # Evolution du vent
    axs[2].plot(filtered["date_time"], filtered["wind"], marker="o", linestyle="-", color="green")
    axs[2].set_ylabel("Vitesse du vent (m/s)")
    axs[2].set_title("Évolution du vent")

    # Evolution de l'humidité
    axs[3].plot(filtered["date_time"], filtered["humidity"], marker="o", linestyle="-", color="purple")
    axs[3].set_ylabel("Humidité (%)")
    axs[3].set_title("Évolution de l'humidité")

    # Evolution de la pression
    axs[4].plot(filtered["date_time"], filtered["pressure"], marker="o", linestyle="-", color="orange")
    axs[4].set_ylabel("Pression (hPa)")
    axs[4].set_title("Évolution de la pression")

    plt.xlabel("Date et Heure")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
