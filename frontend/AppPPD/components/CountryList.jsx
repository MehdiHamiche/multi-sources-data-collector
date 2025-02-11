import React from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';

const CountryList = ({ countries }) => {
  if (!countries || !Array.isArray(countries)) {
    return <Text style={styles.message}>Aucune liste de pays disponible</Text>;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Liste des pays</Text>
      <FlatList
        data={countries}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <Text style={styles.item}>{item.name || 'Pays inconnu'}</Text>
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

export default CountryList;
