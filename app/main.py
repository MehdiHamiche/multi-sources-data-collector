from fastapi import FastAPI, Query
from ariadne.asgi import GraphQL
from datetime import datetime
from app.weather_api import get_weather
from app.electricity_api import get_carbon_intensity, get_power_consumption  # Importer la nouvelle fonction
from app.electricity_api import fetch_all_zones
from app.database import save_to_db
from app.database import get_data_by_time_range
from app.database import create_carbon_countries_table
from app.console_display import display_carbon_data  # Importer l'affichage coloré
from app.console_display import display_all_countries
from app.graphql_schema import schema
from apscheduler.schedulers.background import BackgroundScheduler
from app.graphql_schema import schema

app = FastAPI()

# Appeler la fonction au démarrage
create_carbon_countries_table()

# Fonction pour exécuter les appels API
def scheduled_job():
    city = "Paris"
    weather = get_weather(city)
    carbon = get_carbon_intensity("FR")
    power = get_power_consumption("FR")

    if weather and carbon and power:
        aggregated_data = {
            "city": weather["city"],
            "temperature": weather["temperature"],
            "carbon_intensity": carbon["carbon_intensity"],
            "power_consumption": power["power_Consumption_Breakdown"],
            "power_production": power["power_Production_Breakdown"],
            "date_time": weather["date_time"]
        }
        save_to_db(aggregated_data)
        print("Data saved automatically.")

# Lancer le CRON job
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_job, 'interval', minutes=1)
scheduler.start()

# Endpoint REST pour récupérer les données et les sauvegarder
@app.get("/get-data")
def get_data(city: str):
    weather = get_weather(city)
    carbon = get_carbon_intensity("FR")
    power = get_power_consumption("FR")

    if not weather or not carbon or not power:
        return {"error": "Unable to retrieve data"}

    aggregated_data = {
        "city": weather["city"],
        "temperature": weather["temperature"],
        "carbon_intensity": carbon["carbon_intensity"],
        "power_consumption": power["power_Consumption_Breakdown"],
        "power_production": power["power_Production_Breakdown"],
        "date_time": weather["date_time"]
    }

    save_to_db(aggregated_data)
    return {"message": "Data saved successfully", "data": aggregated_data}

# Endpoint pour filtrer les données par plage horaire
@app.get("/filter-data")
def filter_data(
    start_time: str = Query(..., description="Date de début au format YYYY-MM-DD HH:MM:SS"),
    end_time: str = Query(..., description="Date de fin au format YYYY-MM-DD HH:MM:SS")
):
    try:
        start_time_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

        results = get_data_by_time_range(start_time_dt, end_time_dt)

        if not results:
            return {"message": "Aucune donnée trouvée dans cette plage horaire."}

        return {"filtered_data": results}

    except ValueError:
        return {"error": "Format de date invalide. Utilisez YYYY-MM-DD HH:MM:SS"}

# Endpoint pour afficher les données avec des couleurs dans la console
@app.get("/display-data")
def display_data(
    start_time: str = Query(..., description="Date de début au format YYYY-MM-DD HH:MM:SS"),
    end_time: str = Query(..., description="Date de fin au format YYYY-MM-DD HH:MM:SS")
):
    try:
        start_time_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

        results = get_data_by_time_range(start_time_dt, end_time_dt)

        if not results:
            return {"message": "Aucune donnée trouvée."}

        print("\n📊 **Affichage des données avec couleurs** 📊\n")
        display_carbon_data(results)  # Affichage en couleur
        return {"message": "Données affichées en console"}

    except ValueError:
        return {"error": "Format de date invalide. Utilisez YYYY-MM-DD HH:MM:SS"}

# Endpoint pour afficher la consommation et production d'énergie de toutes les zones
@app.get("/display-power-data")
def display_power_data():
    """
    Affiche la consommation et production d'énergie pour la France.
    """
    print("\n⚡ **Affichage de la consommation et production d'énergie** ⚡\n")
    power_data = get_power_consumption("FR")
    if not power_data:
        return {"error": "Impossible de récupérer les données de consommation/production"}

    print(f"🔌 Consommation : {power_data['power_Consumption_Breakdown']} MW")
    print(f"⚡ Production : {power_data['power_Production_Breakdown']} MW")
    return {"message": "Données affichées en console"}

# Afficher les données de tous les pays
@app.get("/display-all-countries")
def display_countries():
    """
    Affiche tous les pays et leurs niveaux d’intensité carbone.
    """
    print("\n🌍 **Affichage des intensités carbone pour tous les pays du monde** 🌍\n")
    display_all_countries()
    
    return {"message": "Données affichées en console"}

# Event au démarrage pour récupérer les données pour la France et la Corse
@app.on_event("startup")
def startup_event():
    print("🔄 Récupération des données pour la France et la Corse...")
    fetch_all_zones()

# Endpoint GraphQL
app.mount("/graphql", GraphQL(schema))
