import React, { useEffect, useState } from "react";
import { View, Text, TextInput, Button, StyleSheet, ActivityIndicator } from "react-native";
import Header from './components/Header';
import Map from './components/Map';
import CarbonIntensityChart from './components/CarbonIntensityChart';
import CountryList from './components/CountryList';

export default function App() {
  const [city, setCity] = useState(""); // Stocke la ville entrée
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchData = () => {
    if (!city) return; // Vérifie que la ville n'est pas vide
    setLoading(true);

    fetch(`http://192.168.1.120:8000/get-data?city=${city}`)
      .then((response) => response.json())
      .then((json) => {
        setData(json.data);
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

      {/* Champ de saisie pour la ville */}
      <TextInput
        style={styles.input}
        placeholder="Entrez une ville..."
        value={city}
        onChangeText={setCity}
      />
      
      {/* Bouton pour déclencher la recherche */}
      <Button title="Rechercher" onPress={fetchData} />

      {/* Affichage des données */}
      {loading ? (
        <ActivityIndicator size="large" color="#0000ff" />
      ) : data ? (
        <View>
          <Text style={styles.title}>🌍 {data.city}</Text>
          <Text>🌡 Température : {data.temperature}°C</Text>
          <Text>💨 Intensité Carbone : {data.carbon_intensity} gCO₂/kWh</Text>
          <Text>⏳ Date : {data.date_time}</Text>

          {/* Composants supplémentaires */}
          <Map city={data.city} />
          <CarbonIntensityChart data={data} />
          <CountryList />
        </View>
      ) : (
        <Text>❌ Aucune donnée disponible</Text>
      )}
    </View>
  );
}

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
  title: {
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 10,
  },
});
