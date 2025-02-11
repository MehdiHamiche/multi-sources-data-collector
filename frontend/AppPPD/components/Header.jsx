import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const Header = () => {
  return (
    <View style={styles.header}>
      <Text style={styles.title}>Visualisation de l'Intensité Carbone</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  header: {
    backgroundColor: '#282c34',
    padding: 20,
    alignItems: 'center',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: 'white',
  },
});

export default Header;
