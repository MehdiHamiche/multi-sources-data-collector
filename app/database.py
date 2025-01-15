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