import React, { useEffect, useState } from "react";
import { View, Text, FlatList, ActivityIndicator, StyleSheet } from "react-native";
import { useLocalSearchParams } from "expo-router";

export default function CountryListScreen() {
  const { city } = useLocalSearchParams();
  const [countries, setCountries] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`http://192.168.1.120:8000/get-countries?city=${city}`)
      .then((response) => response.json())
      .then((json) => {
        setCountries(json.countries || []);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Erreur de chargement des pays :", error);
        setLoading(false);
      });
  }, [city]);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>🌍 Pays voisins de {city}</Text>
      {loading ? (
        <ActivityIndicator size="large" color="#0000ff" />
      ) : countries.length > 0 ? (
        <FlatList
          data={countries}
          keyExtractor={(item, index) => index.toString()}
          renderItem={({ item }) => <Text style={styles.country}>{item}</Text>}
        />
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
    padding: 20,
  },
  title: {
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 10,
  },
  country: {
    fontSize: 18,
    marginVertical: 5,
  },
});
