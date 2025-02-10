import json
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import duckdb

# Charger les variables d'environnement
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

CITY = ["Paris"]


def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()

        date_time = datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')

        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "date_time": date_time,
            "weather_description": data["weather"][0]["main"],
            "clouds" : data["clouds"]["all"]
        }

        return weather_info
    else:
        print(f"❌ Erreur API ({response.status_code}): {response.text}")
        return None


# Fonction pour récupérer et stocker les données météo des villes
def fetch_weather_infos():
    try:
        conn = duckdb.connect("data.db", read_only=False)

        # ✅ Création de la table avec `TEXT` pour stocker du JSON en tant que string
        conn.execute("""
            CREATE TABLE IF NOT EXISTS weather_infos (
                city TEXT,
                temperature FLOAT,
                dateTime TIMESTAMP,
                description TEXT,
                cloud INTEGER     
            )
        """)

        for city_name in CITY:
            weather_data = get_weather(city_name)
            if weather_data:
                print(f"📊 Ville : {weather_data['city']} - Température : {weather_data['temperature']} °C - Date : {weather_data['date_time']} - Description : {weather_data['weather_description']} - Couverture nuageuse : {weather_data['clouds']}")

                # ✅ Insertion propre des données
                conn.execute("INSERT INTO weather_infos VALUES (?, ?, ?, ?, ?)", 
                             (weather_data["city"], weather_data["temperature"], weather_data["date_time"], weather_data["weather_description"], weather_data["clouds"]))

    except duckdb.IOException as e:
        print(f"❌ Erreur DuckDB : {e}")

    finally:
        conn.close()
