import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    date_time = datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
    weather_info = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "date_time": date_time
    }

    return weather_info