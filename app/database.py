import duckdb

# Fonction pour enregistrer les données dans DuckDB
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


# Fonction pour récupérer les données entre deux dates
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


def create_carbon_countries_table():
    conn = duckdb.connect("data.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS carbon_countries (
            country VARCHAR,
            carbon_intensity FLOAT,
            date_time TIMESTAMP
        )
    """)
    conn.close()

# Lancer cette fonction une seule fois pour créer la table
create_carbon_countries_table()