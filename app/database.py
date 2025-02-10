import duckdb



def save_to_db(data):
    # Connexion à la base de données DuckDB
    conn = duckdb.connect("data.db")

    # Création de la table si elle n'existe pas déjà
    conn.execute("""
        CREATE TABLE IF NOT EXISTS aggregated_data (
            city VARCHAR,
            temperature FLOAT,
            carbon_intensity FLOAT,
            date_time TIMESTAMP
        )
    """)


    # Insérer les données dans la table
    conn.execute("""
        INSERT INTO aggregated_data (city, temperature, carbon_intensity, date_time)
        VALUES (?, ?, ?, ?)
    """, (data["city"], data["temperature"], data["carbon_intensity"], data["date_time"]))

    # Fermer la connexion à la base de données
    conn.close()



# Fonction pour récupérer les données entre deux dates (table aggregated_data)
def get_data_by_time_range(start_time, end_time):
    try:
        conn = duckdb.connect("data.db", read_only=True)

        query = """
            SELECT * FROM aggregated_data
            WHERE date_time BETWEEN CAST(? AS TIMESTAMP) AND CAST(? AS TIMESTAMP)
            ORDER BY date_time ASC
        """
        results = conn.execute(query, (start_time, end_time)).fetchall()

        return results

    except duckdb.IOException as e:
        print(f"❌ Erreur DuckDB : {e}")
        return None

    finally:
        conn.close()


# Fonction pour créer la table carbon_countries avec les nouvelles colonnes
def create_carbon_countries_table():
    conn = duckdb.connect("data.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS carbon_countries (
            country VARCHAR,
            carbon_intensity FLOAT,
            date_time TIMESTAMP,
        )
    """)
    conn.close()


# Fonction pour récupérer et stocker les données des zones françaises
def fetch_all_zones(ZONES_FRANCE, get_carbon_intensity, get_power_consumption):
    try:
        conn = duckdb.connect("data.db", read_only=False)

        # Assurer que la table `carbon_zones` est bien créée avec les champs de consommation et production
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
                conn.execute("""
                    INSERT INTO carbon_zones (zone, carbon_intensity, datetime)
                    VALUES (?, ?, ?)
                """, (
                    zone_name,
                    carbon_data["carbon_intensity"],
                    carbon_data["datetime"]
                ))

    except duckdb.IOException as e:
        print(f"❌ Erreur DuckDB : {e}")

    finally:
        conn.close()  # Fermeture propre de la connexion


# Lancer cette fonction une seule fois pour créer la table carbon_countries
create_carbon_countries_table()
