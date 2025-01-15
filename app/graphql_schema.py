import duckdb
from ariadne import QueryType, make_executable_schema

# Définir le type GraphQL
type_defs = """
    type Query {
        getData(city: String!): AggregatedData
    }

    type AggregatedData {
        city: String
        temperature: Float
        carbonIntensity: Float
        dateTime: String
    }
"""

# Définir la logique pour résoudre la requête getData
query = QueryType()

@query.field("getData")
def resolve_get_data(_, info, city):
    conn = duckdb.connect("data.db")
    result = conn.execute(
        "SELECT city, temperature, carbon_intensity, date_time FROM aggregated_data WHERE city = ?", [city]
    ).fetchone()

    if result:
        return {
            "city": result[0],
            "temperature": result[1],
            "carbonIntensity": result[2],
            "dateTime": result[3].strftime('%Y-%m-%d %H:%M:%S')
        }
    return None

# Créer le schéma exécutable
schema = make_executable_schema(type_defs, query)