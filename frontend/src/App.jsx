import React from 'react';
import Header from './components/Header';
import Map from './components/Map';
import CarbonIntensityChart from './components/CarbonIntensityChart';
import CountryList from './components/CountryList';
import './styles/App.css';

const App = () => {
  return (
    <div className="App">
      <Header />
      <div className="content">
        <Map />
        <CarbonIntensityChart />
        <CountryList />
      </div>
    </div>
  );
};

export default App;