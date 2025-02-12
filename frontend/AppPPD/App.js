import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

// Import des écrans
import HomeScreen from "./screens/HomeScreen";
import MapScreen from "./screens/MapScreen";
import ChartScreen from "./screens/ChartScreen";
import CountryListScreen from "./screens/CountryListScreen";

// Création du stack navigator
const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Accueil" component={HomeScreen} />
        <Stack.Screen name="Carte" component={MapScreen} />
        <Stack.Screen name="Graphique" component={ChartScreen} />
        <Stack.Screen name="Pays" component={CountryListScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
