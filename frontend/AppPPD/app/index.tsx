import React from "react";
import { View, Text, Button, StyleSheet } from "react-native";
import { useRouter } from "expo-router";
import Header from "../components/Header";

export default function HomeScreen() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <Header />
      <Text style={styles.title}>Bienvenue !</Text>

      {/* Bouton pour aller sur la page des informations de ville */}
      <Button title="Rechercher une Ville" onPress={() => router.push("./city-info")} />

      {/* Autres boutons */}
      <Button title="Voir la Carte" onPress={() => router.push("./map")} />
      <Button title="Voir les Graphiques" onPress={() => router.push("./chart")} />
      <Button title="Voir la Liste des Pays" onPress={() => router.push("./country-list")} />
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
  title: {
    fontSize: 22,
    fontWeight: "bold",
    marginBottom: 10,
  },
});
