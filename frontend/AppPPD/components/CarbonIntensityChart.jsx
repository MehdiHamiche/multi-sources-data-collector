import React from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';

const CarbonIntensityChart = ({ data }) => {
  if (!data || !Array.isArray(data)) {
    return <Text style={styles.message}>Aucune donnée disponible</Text>;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Graphique de l'intensité carbone</Text>
      <FlatList
        data={data}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <Text style={styles.item}>
            {item.time}: {item.intensity}
          </Text>
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 20,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  item: {
    fontSize: 16,
    padding: 5,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
  },
  message: {
    textAlign: 'center',
    marginTop: 20,
  },
});

export default CarbonIntensityChart;
