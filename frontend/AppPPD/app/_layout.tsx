import { Stack } from "expo-router";

export default function Layout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: "Home" }} />
      <Stack.Screen name="map" options={{ title: "Map" }} />
      <Stack.Screen name="chart" options={{ title: "Intensity Carbon Grapics" }} />
      <Stack.Screen name="country-list" options={{ title: "Country List" }} />
    </Stack>
  );
}
