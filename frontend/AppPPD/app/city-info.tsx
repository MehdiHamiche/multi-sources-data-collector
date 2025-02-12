import React, { useEffect, useState } from "react";
import { View, Text, TextInput, Button, ActivityIndicator, StyleSheet } from "react-native";
import { useRouter } from "expo-router";
import Header from "../components/Header";
import CarbonIntensityChart from "../components/CarbonIntensityChart";
import CountryList from "../components/CountryList";

interface CityData {
  city: string;
  temperature: number;
  carbon_intensity: number;
  date_time: string;
  latitude?: number;
  longitude?: number;
  history?: { date: string; carbon_intensity: number }[];
  countries?: string[];
}

export default function CityInfoScreen() {
  const [city, setCity] = useState("");
  const [data, setData] = useState<CityData | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const fetchData = () => {
    if (!city) return;
    setLoading(true);

    fetch(`http://192.168.1.120:8000/get-data?city=${city}`)
      .then((response) => response.json())
      .then((json) => {
        console.log("Données reçues :", json); // 🔥 Vérification des données reçues
        setData(json.data || null);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Erreur de chargement des données :", error);
        setLoading(false);
      });
  };

  return (
    <View style={styles.container}>
      <Header />

      {/* Champ de saisie pour entrer la ville */}
      <TextInput
        style={styles.input}
        placeholder="Entrez une ville..."
        value={city}
        onChangeText={setCity}
      />

      {/* Bouton de recherche */}
      <Button title="Rechercher" onPress={fetchData} />

      {/* Affichage des résultats */}
      {loading ? (
        <ActivityIndicator size="large" color="#0000ff" />
      ) : data ? (
        <View style={styles.dataContainer}>
          <Text style={styles.cityTitle}>🌍 {data.city}</Text>
          <Text>🌡 Température : {data.temperature}°C</Text>
          <Text>💨 Intensité Carbone : {data.carbon_intensity} gCO₂/kWh</Text>
          <Text>⏳ Date : {data.date_time}</Text>

          {/* Bouton pour afficher la carte uniquement si on a latitude & longitude */}
          {data.latitude !== undefined && data.longitude !== undefined ? (
            <Button
              title="📍 Voir la carte"
              onPress={() => router.push(`/map?latitude=${data.latitude}&longitude=${data.longitude}&city=${data.city}`)}
            />
          ) : (
            <Text>📍 Aucune localisation disponible</Text>
          )}

          {/* Vérification avant d'afficher le graphique */}
          {data.history && Array.isArray(data.history) && data.history.length > 0 ? (
            <CarbonIntensityChart data={data.history} />
          ) : (
            <Text>📉 Aucune donnée historique disponible</Text>
          )}

          {/* Vérification avant d'afficher la liste des pays */}
          {data.countries && data.countries.length > 0 ? (
            <CountryList countries={data.countries} />
          ) : (
            <Text>🌍 Aucune information sur les pays voisins</Text>
          )}
        </View>
      ) : (
        <Text>❌ Aucune donnée disponible</Text>
      )}
    </View>
  );
}

// Styles
const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#fff",
    padding: 20,
  },
  input: {
    borderWidth: 1,
    borderColor: "#ccc",
    padding: 10,
    marginVertical: 10,
    width: "80%",
    borderRadius: 5,
  },
  cityTitle: {
    fontSize: 20,
    fontWeight: "bold",
    marginVertical: 10,
  },
  dataContainer: {
    marginTop: 20,
    alignItems: "center",
  },
});
