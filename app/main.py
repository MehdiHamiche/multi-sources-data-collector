import csv
from fastapi import FastAPI, Query
from ariadne.asgi import GraphQL
from datetime import datetime
from app.weather_api import get_weather
from app.weather_api import fetch_weather_infos
from app.electricity_api import get_carbon_intensity, get_power_consumption  # Importer la nouvelle fonction
from app.electricity_api import fetch_all_zones
from app.electricity_api import fetch_consumption_zones
from app.database import save_to_db, new_to_db
from app.database import get_data_by_time_range
from app.database import create_carbon_countries_table
from app.database import export_to_csv
from app.console_display import display_carbon_data  # Importer l'affichage coloré
from app.console_display import display_all_countries
from app.graphql_schema import schema
from apscheduler.schedulers.background import BackgroundScheduler
from app.graphql_schema import schema

app = FastAPI()

# Appeler la fonction au démarrage
create_carbon_countries_table()

# 📌 Fonction pour lire `weather_infos.csv`
def read_weather_data():
    data = []
    with open("weather_infos.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({
                "city": row["city"],
                "temperature": float(row["temperature"]),
                "dateTime": row["dateTime"],
                "description": row["description"],
                "cloud": int(row["cloud"]),
                "wind": float(row["wind"]),
                "humidity": int(row["humidity"]),
                "pressure": int(row["pressure"])
            })
    return data

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
        new_to_db(aggregated_data)
        print("Data saved automatically.")

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_job, 'interval', minutes=1)
scheduler.start()

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
    new_to_db(aggregated_data)
    return {"message": "Data saved successfully", "data": aggregated_data}

@app.get("/get-weather-data")
def get_weather_data():
    weather_data = read_weather_data()
    print("📡 Données envoyées à l'application :", weather_data)
    return JSONResponse(content={"history": weather_data})

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



@app.get("/display-weather-data")
def display_weather_data():
    """
    Affiche la descriptyion du temps en France.
    """
    print("\n **Affichage des infos** \n")
    weather_data = get_weather("Paris")
    if not weather_data:
        return {"error": "Impossible de récupérer les données de consommation/production"}

    print(f" Ville : {weather_data['city']}")
    print(f" Temperature : {weather_data['temperature']}")
    print(f" Date actuelle : {weather_data['date_time']}")
    print(f" Description du temps : {weather_data['weather_description']}")
    print(f" Couverture nuageuse : {weather_data['clouds']}")
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
    fetch_consumption_zones()
    fetch_weather_infos()
    export_to_csv()
# Endpoint GraphQL
app.mount("/graphql", GraphQL(schema))
