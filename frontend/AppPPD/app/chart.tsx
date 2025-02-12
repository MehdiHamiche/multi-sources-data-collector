import React, { useEffect, useState } from "react";
import { View, Text, ActivityIndicator, StyleSheet } from "react-native";
import { LineChart } from "react-native-chart-kit";

export default function ChartScreen() {
  const [data, setData] = useState<{ date: string; carbon_intensity: number }[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://192.168.1.120:8000/get-carbon-history")
      .then((response) => response.json())
      .then((json) => {
        console.log("📊 Données reçues :", json);
        setData(json.history || []);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Erreur chargement des données :", error);
        setLoading(false);
      });
  }, []);

  if (loading) return <ActivityIndicator size="large" color="#0000ff" />;

  return (
    <View style={styles.container}>
      <Text style={styles.title}>📊 Historique de l’intensité carbone</Text>
      {data.length > 0 ? (
        <LineChart
          data={{
            labels: data.map((d) => d.date),
            datasets: [{ data: data.map((d) => d.carbon_intensity) }],
          }}
          width={350}
          height={220}
          yAxisSuffix=" gCO₂/kWh"
          chartConfig={{
            backgroundColor: "#f2f2f2",
            backgroundGradientFrom: "#fff",
            backgroundGradientTo: "#ddd",
            decimalPlaces: 0,
            color: (opacity = 1) => `rgba(0, 0, 255, ${opacity})`,
          }}
          style={styles.chart}
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
    backgroundColor: "#fff",
    padding: 20,
  },
  title: {
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 10,
  },
  chart: {
    marginVertical: 20,
  },
});
