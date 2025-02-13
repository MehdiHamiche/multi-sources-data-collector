import React, { useEffect, useState } from 'react';
import { SafeAreaView, Text, ScrollView } from 'react-native';
import { CartesianChart, Bar } from 'victory-native';
import Papa from 'papaparse';
import * as FileSystem from 'expo-file-system';
import { Asset } from 'expo-asset';

type CSVData = {
  dateTime: string;
  temperature: number;
  // autres colonnes si nécessaire
};

export default function CSVBarChart() {
  const [data, setData] = useState<CSVData[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Charger le fichier CSV en utilisant expo-asset
        const asset = Asset.fromModule(require('../../weather_infos.csv'));
        await asset.downloadAsync(); // S'assurer que l'asset est téléchargé
        const csvUri = asset.uri;

        // Lire le fichier CSV via expo-file-system
        const fileString = await FileSystem.readAsStringAsync(csvUri);

        // Parser le CSV avec PapaParse
        Papa.parse(fileString, {
          header: true,
          dynamicTyping: true,
          complete: (result: any) => {
            console.log("Données CSV :", result.data);
            setData(result.data);
          },
        });
      } catch (error) {
        console.error("Erreur lors du chargement du CSV :", error);
      }
    };

    fetchData();
  }, []);

  return (
    <SafeAreaView style={{ flex: 1, padding: 20 }}>
      <Text style={{ fontSize: 20, fontWeight: 'bold', marginBottom: 20 }}>
        Graphique de l'Intensité Carbone
      </Text>
      
      {/* Affichage du graphique */}
      {data.length > 0 ? (
        <CartesianChart data={data} xKey="dateTime" yKeys={['temperature']}>
          {({ points, chartBounds }) => (
            <Bar
              points={points.temperature}
              chartBounds={chartBounds}
              color="tomato"
              roundedCorners={{ topLeft: 10, topRight: 10 }}
            />
          )}
        </CartesianChart>
      ) : (
        <Text>Chargement des données pour le graphique...</Text>
      )}

      {/* Affichage de la liste des données pour le débogage */}
      <ScrollView style={{ marginTop: 20 }}>
        {data.length > 0 ? (
          data.map((item, index) => (
            <Text key={index}>
              {item.dateTime} - {item.temperature}
            </Text>
          ))
        ) : (
          <Text>Chargement des données...</Text>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}
