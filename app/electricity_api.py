import requests
import os
import duckdb
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
API_KEY = os.getenv("ELECTRICITYMAP_API_KEY")
# Afficher la clé API utilisée
print(f"Clé API utilisée : {API_KEY}")

# Liste des zones valides en France selon l'API Electricity Map
ZONES_FRANCE = {
    "France Métropolitaine": "FR",
    "Corse": "FR-COR"
}

# Fonction pour récupérer l'intensité carbone pour une zone donnée
def get_carbon_intensity(zone_code):
    url = f"https://api.electricitymap.org/v3/carbon-intensity/latest?zone={zone_code}"
    headers = {"auth-token": API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return {
            "zone": zone_code,
            "carbon_intensity": data["carbonIntensity"],
            "datetime": data["datetime"]
        }
    else:
        print(f"❌ Erreur {response.status_code} - {response.text}")
        return None

def get_power_consumption(zone_code):
    url = f"https://api.electricitymap.org/v3/power-breakdown/latest?zone={zone_code}"
    headers = {"auth-token": API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return {
            "zone": zone_code,
            "power_Consumption_Breakdown": data["powerConsumptionBreakdown"],
            "power_Production_Breakdown": data["powerProductionBreakdown"],
            "datetime": data["datetime"]
        }
    else:
        print(f"❌ Erreur {response.status_code} - {response.text}")
        return None


# Fonction pour récupérer et stocker les données des zones françaises
def fetch_all_zones():
    try:
        conn = duckdb.connect("data.db", read_only=False)

        # 🔴 Assurer que la table `carbon_zones` est bien créée
        conn.execute("""
            CREATE TABLE IF NOT EXISTS carbon_zones (
                zone TEXT,
                carbon_intensity FLOAT,
                datetime TIMESTAMP
            )
        """)

        for zone_name, zone_code in ZONES_FRANCE.items():
            carbon_data = get_carbon_intensity(zone_code)
            power_data = get_power_consumption(zone_code)
            if carbon_data and power_data:
                print(f"📊 Zone : {zone_name} - Intensité carbone : {carbon_data['carbon_intensity']} gCO₂/kWh - Date : {carbon_data['datetime']}")
                print(f"Production : {power_data['power_Consumption_Breakdown']} MW - Demande : {power_data['power_Production_Breakdown']} MW")
                conn.execute("INSERT INTO carbon_zones VALUES (?, ?, ?)", 
                             (zone_name, carbon_data["carbon_intensity"], carbon_data["datetime"]))

    except duckdb.IOException as e:
        print(f"❌ Erreur DuckDB : {e}")

    finally:
        conn.close()  # 🔴 Fermeture propre de la connexion


# Fonction pour récupérer toutes les zones disponibles
def get_available_zones():
    """
    Récupère toutes les zones (pays & régions) disponibles via l'API Electricity Map.
    """
    url = "https://api.electricitymap.org/v3/zones"
    headers = {"auth-token": API_KEY}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Retourne toutes les zones sous forme de dictionnaire
    else:
        print(f"❌ Erreur lors de la récupération des zones : {response.status_code} - {response.text}")
        return None
    

# 🔹 Fonction pour récupérer et stocker l’intensité carbone de tous les pays
def fetch_all_countries():
    """
    Récupère et stocke l'intensité carbone de tous les pays disponibles.
    """
    # Obtenir la liste des zones disponibles
    url = "https://api.electricitymap.org/v3/zones"
    headers = {"auth-token": API_KEY}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Erreur lors de la récupération des zones : {response.status_code} - {response.text}")
        return
    
    zones = response.json()  # Stocker la réponse JSON
    conn = duckdb.connect("data.db")

    # 🔹 Vérifier que la table `carbon_countries` existe bien
    conn.execute("""
        CREATE TABLE IF NOT EXISTS carbon_countries (
            country VARCHAR,
            carbon_intensity FLOAT,
            datetime TIMESTAMP
        )
    """)

    # 🔹 Récupérer et stocker l’intensité carbone pour chaque pays
    for zone_code, zone_info in zones.items():
        country_name = zone_info.get("countryName", zone_code)  # Prend le nom du pays ou code s'il n'existe pas
        
        data = get_carbon_intensity(zone_code)
        if data:
            conn.execute("INSERT INTO carbon_countries VALUES (?, ?, ?)",
                         (country_name, data["carbon_intensity"], data["datetime"]))
            print(f"🌍 {country_name} | 💨 CO₂: {data['carbon_intensity']} gCO₂/kWh | ⏳ {data['datetime']}")

    conn.close()