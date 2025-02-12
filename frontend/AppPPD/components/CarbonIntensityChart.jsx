import React from "react";
import { View, Text, Dimensions } from "react-native";
import { LineChart } from "react-native-chart-kit";

const CarbonIntensityChart = ({ data }) => {
  if (!data || data.length === 0) {
    return <Text>Aucune donnée disponible</Text>;
  }

  const labels = data.map(item => item.date_time);
  const values = data.map(item => item.carbon_intensity);

  return (
    <View>
      <Text style={{ textAlign: "center", fontSize: 16, marginBottom: 10 }}>
        Intensité carbone sur le temps
      </Text>
      <LineChart
        data={{
          labels: labels,
          datasets: [{ data: values }]
        }}
        width={Dimensions.get("window").width - 20}
        height={220}
        yAxisSuffix=" gCO₂/kWh"
        chartConfig={{
          backgroundColor: "#e26a00",
          backgroundGradientFrom: "#ff9800",
          backgroundGradientTo: "#ffcc80",
          decimalPlaces: 2,
          color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
          labelColor: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
        }}
        bezier
      />
    </View>
  );
};

export default CarbonIntensityChart;
