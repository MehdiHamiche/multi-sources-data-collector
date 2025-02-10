import React from 'react';
import Header from './components/Header';
import Map from './components/Map';
import CarbonIntensityChart from './components/CarbonIntensityChart';
import CountryList from './components/CountryList';
import './styles/App.css';

function App() {
  return (
    <div className="App">
      {/* En-tête de l'application */}
      <Header />

      {/* Contenu principal */}
      <div className="content">
        {/* Section pour la carte */}
        <section className="map-section">
          <h2>Carte de l'Intensité Carbone</h2>
          <Map />
        </section>

        {/* Section pour le graphique */}
        <section className="chart-section">
          <h2>Intensité Carbone au fil du temps</h2>
          <CarbonIntensityChart />
        </section>

        {/* Section pour la liste des pays */}
        <section className="country-list-section">
          <h2>Intensité Carbone par Pays</h2>
          <CountryList />
        </section>
      </div>
    </div>
  );
}

export default App;
