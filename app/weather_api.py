import csv
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

def get_weather(city, output_file="weather_data.csv"):
    # Charger les variables d'environnement
    load_dotenv()
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    if not API_KEY:
        print("❌ API_KEY introuvable. Vérifiez votre fichier .env.")
        return None

    # Récupérer les données météo via l'API OpenWeatherMap
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"❌ Erreur API ({response.status_code}): {response.text}")
        return None

    data = response.json()
    date_time = datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')

    weather_info = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "date_time": date_time,
        "weather_description": data["weather"][0]["main"],
        "clouds": data["clouds"]["all"],
        "wind": data["wind"]["speed"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"]
    }

    # Définir le dossier de sortie : app/data_csv
    output_dir = os.path.join("app", "data_csv")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Chemin complet du fichier CSV
    output_path = os.path.join(output_dir, output_file)
    file_exists = os.path.exists(output_path)

    # Exporter les données dans le fichier CSV
    with open(output_path, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "city", "temperature", "date_time", "weather_description",
            "clouds", "wind", "humidity", "pressure"
        ])
        if not file_exists:
            writer.writeheader()
        writer.writerow(weather_info)

    print(f"✅ Données météo sauvegardées dans {output_path}")
    return weather_info

def fetch_weather_infos():
    try:
        conn = duckdb.connect("data.db", read_only=False)

        # Supprimer la table existante si elle existe pour recréer le schéma correct
        conn.execute("DROP TABLE IF EXISTS weather_infos")

        # Créer la table avec 8 colonnes
        conn.execute("""
            CREATE TABLE IF NOT EXISTS weather_infos (
                city TEXT,
                temperature FLOAT,
                dateTime TIMESTAMP,
                description TEXT,
                clouds INTEGER,
                wind FLOAT,
                humidity INTEGER,
                pressure INTEGER    
            )
        """)

        for city_name in CITY:
            weather_data = get_weather(city_name)
            if weather_data:
                print(f"📊 Ville : {weather_data['city']} - Température : {weather_data['temperature']} °C - Date : {weather_data['date_time']} - Description : {weather_data['weather_description']} - Couverture nuageuse : {weather_data['clouds']}")
                conn.execute("INSERT INTO weather_infos VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                             (weather_data["city"], 
                              weather_data["temperature"], 
                              weather_data["date_time"], 
                              weather_data["weather_description"], 
                              weather_data["clouds"], 
                              weather_data["wind"],
                              weather_data["humidity"], 
                              weather_data["pressure"]))
    except duckdb.IOException as e:
        print(f"❌ Erreur DuckDB : {e}")
    finally:
        conn.close()

# Appel de la fonction pour récupérer et stocker les données météo
fetch_weather_infos()
