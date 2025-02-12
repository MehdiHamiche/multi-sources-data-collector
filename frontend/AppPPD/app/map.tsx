import React from "react";
import { View, Text, StyleSheet } from "react-native";
import MapView, { Marker } from "react-native-maps";
import { useLocalSearchParams } from "expo-router";

export default function MapScreen() {
  const { latitude, longitude, city } = useLocalSearchParams();

  // 🔥 Convertir `latitude` et `longitude` en `number`
  const lat = Array.isArray(latitude) ? parseFloat(latitude[0]) : parseFloat(latitude);
  const lon = Array.isArray(longitude) ? parseFloat(longitude[0]) : parseFloat(longitude);
  const cityName = Array.isArray(city) ? city[0] : city;

  // 🔥 Vérifier si lat/lon sont bien valides
  if (isNaN(lat) || isNaN(lon)) {
    return (
      <View style={styles.container}>
        <Text>❌ Aucune donnée GPS disponible</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>🗺 Carte de {cityName}</Text>
      <MapView
        style={styles.map}
        initialRegion={{
          latitude: lat,
          longitude: lon,
          latitudeDelta: 0.1,
          longitudeDelta: 0.1,
        }}
      >
        <Marker
          coordinate={{ latitude: lat, longitude: lon }}
          title={cityName || "Ville inconnue"}
          description="Localisation de la ville"
        />
      </MapView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  title: {
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 10,
  },
  map: {
    width: "100%",
    height: "80%",
  },
});
