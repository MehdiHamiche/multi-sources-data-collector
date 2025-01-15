import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Clé d'API pour ElectricityMap
API_KEY = os.getenv("ELECTRICITYMAP_API_KEY")

# Fonction pour récupérer l'intensité carbone
def get_carbon_intensity(zone="FR"):
    url = f"https://api.electricitymap.org/v3/carbon-intensity/latest?zone={zone}"
    headers = {"auth-token": API_KEY}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "zone": data["zone"],
            "carbon_intensity": data["carbonIntensity"],
            "datetime": data["datetime"]
        }
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None