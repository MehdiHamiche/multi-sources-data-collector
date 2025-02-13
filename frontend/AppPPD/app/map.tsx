import React from "react";
import { View, Text, StyleSheet } from "react-native";
import MapView, { Marker } from "react-native-maps";

export default function MapScreen() {
  // 📍 Coordonnées GPS de Paris (OpenWeather)
  const parisRegion = {
    latitude: 48.8566,
    longitude: 2.3522,
    latitudeDelta: 0.1, // Zoom plus précis
    longitudeDelta: 0.1,
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>🗺 Carte de Paris</Text>
      <MapView style={styles.map} initialRegion={parisRegion}>
        <Marker coordinate={parisRegion} title="Paris" description="Capitale de la France" />
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
