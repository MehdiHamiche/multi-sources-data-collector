import React, { useEffect, useState } from "react";
import { View, Text, ActivityIndicator, StyleSheet } from "react-native";
import { LineChart } from "react-native-chart-kit";

interface WeatherData {
  dateTime: string;
  temperature: number;
  cloud: number;
  description: string;
}

export default function CarbonIntensityChart() {
  const [data, setData] = useState<WeatherData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://192.168.1.120:8000/get-weather-data")
      .then((response) => response.json())
      .then((json) => {
        console.log("📊 Données météo reçues :", json);
        if (Array.isArray(json.history)) {
          setData(json.history);
        } else {
          console.error("❌ Format de données incorrect !");
          setData([]);
        }
        setLoading(false);
      })
      .catch((error) => {
        console.error("❌ Erreur de chargement des données :", error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <ActivityIndicator size="large" color="#0000ff" />;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>📊 Température et couverture nuageuse</Text>
      <LineChart
        data={{
          labels: data.map((item) => item.dateTime.split(" ")[1]), // Affiche seulement l'heure
          datasets: [
            { data: data.map((item) => item.temperature), color: (opacity = 1) => `rgba(255, 99, 132, ${opacity})` },
            { data: data.map((item) => item.cloud), color: (opacity = 1) => `rgba(54, 162, 235, ${opacity})` },
          ],
          legend: ["Température (°C)", "Couverture Nuageuse (%)"], // ✅ Utilisation correcte de `legend`
        }}
        width={350}
        height={220}
        yAxisSuffix="%"
        chartConfig={{
          backgroundGradientFrom: "#fff",
          backgroundGradientTo: "#ddd",
          decimalPlaces: 0,
          color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
        }}
        style={styles.chart}
      />
      <View style={styles.legendContainer}>
        {data.map((item, index) => (
          <Text key={index} style={styles.legendText}>
            🕒 {item.dateTime} - 🌡 {item.temperature}°C - ☁ {item.cloud}% ({item.description})
          </Text>
        ))}
      </View>
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
  legendContainer: {
    marginTop: 10,
  },
  legendText: {
    fontSize: 14,
  },
});
