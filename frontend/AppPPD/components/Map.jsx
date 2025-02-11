import React from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';

const Map = ({ data }) => {
  if (!data || !Array.isArray(data)) {
    return <Text style={styles.message}>Aucune donnée disponible</Text>;
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={data}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <Text style={styles.item}>{item.name || 'Lieu inconnu'}</Text>
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 20,
    backgroundColor: '#ddd',
  },
  item: {
    fontSize: 16,
    padding: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
  },
  message: {
    textAlign: 'center',
    marginTop: 20,
  },
});

export default Map;
