import React from 'react';
import { View, StyleSheet } from 'react-native';
import Header from './components/Header';
import Map from './components/Map';
import CarbonIntensityChart from './components/CarbonIntensityChart';
import CountryList from './components/CountryList';

const sampleData = [{ name: 'France' }, { name: 'USA' }, { name: 'Allemagne' }];
const sampleChartData = [
  { time: '10:00', intensity: 50 },
  { time: '11:00', intensity: 60 },
  { time: '12:00', intensity: 45 },
];

export default function App() {
  return (
    <View style={styles.container}>
      <Header />
      <CountryList countries={sampleData} />
      <CarbonIntensityChart data={sampleChartData} />
      <Map data={sampleData} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
});
