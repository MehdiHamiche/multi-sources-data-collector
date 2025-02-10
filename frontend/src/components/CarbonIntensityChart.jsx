import React from 'react';

const CarbonIntensityChart = ({ data }) => {
  if (!data || !Array.isArray(data)) {
    return <p>Aucune donnée disponible</p>;
  }

  return (
    <div>
      <h3>Graphique de l'intensité carbone</h3>
      <ul>
        {data.map((point, index) => (
          <li key={index}>
            {point.time}: {point.intensity}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CarbonIntensityChart;
