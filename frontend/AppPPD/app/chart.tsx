import React from "react";
import { View, StyleSheet } from "react-native";
import CarbonIntensityChart from "../components/CarbonIntensityChart";

export default function ChartScreen() {
  return (
    <View style={styles.container}>
      <CarbonIntensityChart />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#fff",
  },
});
