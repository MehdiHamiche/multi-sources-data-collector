import React from 'react';
import './Map.css';

const Map = ({ data }) => {
  if (!data || !Array.isArray(data)) {
    return <p>Aucune donnée disponible</p>;
  }

  return (
    <div className="map-container">
      <ul>
        {data.map((location, index) => (
          <li key={index}>{location.name || 'Lieu inconnu'}</li>
        ))}
      </ul>
    </div>
  );
};

export default Map;
