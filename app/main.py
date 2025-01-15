from fastapi import FastAPI
from ariadne.asgi import GraphQL
from app.weather_api import get_weather
from app.electricity_api import get_carbon_intensity
from app.database import save_to_db
from app.graphql_schema import schema
from apscheduler.schedulers.background import BackgroundScheduler
from app.graphql_schema import schema

app = FastAPI()

# Fonction pour exécuter les appels API
def scheduled_job():
    city = "Paris"
    weather = get_weather(city)
    carbon = get_carbon_intensity("FR")

    if weather and carbon:
        aggregated_data = {
            "city": weather["city"],
            "temperature": weather["temperature"],
            "carbon_intensity": carbon["carbon_intensity"],
            "date_time": weather["date_time"]
        }
        save_to_db(aggregated_data)
        print("Data saved automatically.")

# Lancer le CRON job
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_job, 'interval', minutes=1)
scheduler.start()

# Endpoint REST
@app.get("/get-data")
def get_data(city: str):
    weather = get_weather(city)
    carbon = get_carbon_intensity("FR")

    if not weather or not carbon:
        return {"error": "Unable to retrieve data"}

    aggregated_data = {
        "city": weather["city"],
        "temperature": weather["temperature"],
        "carbon_intensity": carbon["carbon_intensity"],
        "date_time": weather["date_time"]
    }

    save_to_db(aggregated_data)
    return {"message": "Data saved successfully", "data": aggregated_data}

# Endpoint GraphQL
app.mount("/graphql", GraphQL(schema))