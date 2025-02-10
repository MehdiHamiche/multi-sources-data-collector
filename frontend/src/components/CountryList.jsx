import React from 'react';

const CountryList = ({ countries }) => {
  if (!countries || !Array.isArray(countries)) {
    return <p>Aucune liste de pays disponible</p>;
  }

  return (
    <div>
      <h3>Liste des pays</h3>
      <ul>
        {countries.map((country, index) => (
          <li key={index}>{country.name || 'Pays inconnu'}</li>
        ))}
      </ul>
    </div>
  );
};

export default CountryList;
