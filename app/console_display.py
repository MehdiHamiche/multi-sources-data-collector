import colorama
from colorama import Fore, Style
import duckdb


colorama.init(autoreset=True)  # Active la gestion des couleurs

def get_color_for_carbon_intensity(carbon_intensity):
    """
    Retourne la couleur associée au niveau d'intensité carbone.
    """
    if carbon_intensity > 150:
        return Fore.RED  # 🔴 Rouge : Pollution forte
    elif 100 <= carbon_intensity <= 150:
        return Fore.YELLOW  # 🟠 Orange : Pollution moyenne
    else:
        return Fore.GREEN  # 🟢 Vert : Pollution faible

def display_carbon_data(data):
    """
    Affiche les données en console avec les couleurs appropriées.
    """
    for entry in data:
        city = entry[0]
        temperature = entry[1]
        carbon_intensity = entry[2]
        date_time = entry[3]

        color = get_color_for_carbon_intensity(carbon_intensity)
        print(color + f"📍 {city} | 🌡 Temp: {temperature:.1f}°C | 💨 CO₂: {carbon_intensity} gCO₂/kWh | ⏳ {date_time}")


def display_all_countries():
    """
    Affiche toutes les données des pays enregistrées dans DuckDB avec couleurs.
    """
    conn = duckdb.connect("data.db")
    results = conn.execute("SELECT * FROM carbon_countries").fetchall()
    conn.close()

    if not results:
        print("❌ Aucune donnée trouvée.")
        return

    print("\n🌍 **Affichage des données pour tous les pays** 🌍\n")
    for entry in results:
        country = entry[0]
        carbon_intensity = entry[1]
        date_time = entry[2]

        color = get_color_for_carbon_intensity(carbon_intensity)
        print(color + f"📍 Pays : {country} | 💨 CO₂ : {carbon_intensity} gCO₂/kWh | ⏳ {date_time}")