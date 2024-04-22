import React, { useState } from 'react';
import axios from 'axios';
import USMap from './USMap'; // Import the USMap component

function App() {
  const [term, setTerm] = useState('');
  const [results, setResults] = useState([]);
  const [sort, setSort] = useState('score');
  const [state, setState] = useState('');

  const handleSearch = async () => {
    try {
      const response = await axios.post('http://localhost:5001/api/search/', { term, sort_by: sort, state });
      setResults(response.data);
    } catch (error) {
      console.error("Error during search:", error);
      setResults([]); // Clear results on error or no data
    }
  };

  const handleStateSelect = (stateCode) => {
    setState(stateCode); // Update state with the state code
    handleSearch(); // Trigger search immediately after state selection
  };

  return (
    <div style={{ display: 'flex', padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <div style={{ width: '60%', paddingRight: '20px' }}>
        <h2 style={{ color: '#007BFF', textAlign: 'center' }}>
          {state ? `Recommendations for ${state}` : "Recommendations Overall"}
        </h2>
        <USMap onSelectState={handleStateSelect} /> {/* Ensure onSelectState triggers the state change directly */}
      </div>
      <div style={{ width: '40%' }}>
        <div style={{ marginBottom: '20px' }}>
          <input
            value={term}
            onChange={e => setTerm(e.target.value)}
            placeholder="Enter search term..."
            style={{ width: '100%', padding: '10px', marginBottom: '10px', fontSize: '16px', borderRadius: '5px', border: '1px solid #ccc' }}
          />
          <select
            value={sort}
            onChange={e => setSort(e.target.value)}
            style={{ width: '100%', padding: '10px', marginBottom: '10px', fontSize: '16px', borderRadius: '5px', border: '1px solid #ccc' }}
          >
            <option value="stars">Sort by Stars</option>
            <option value="popularity">Sort by Popularity</option>
          </select>
          <button
            onClick={handleSearch}
            style={{ width: '100%', padding: '10px 20px', fontSize: '16px', backgroundColor: '#007BFF', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}
          >
            Search
          </button>
        </div>
        <ul>
          {results.map((result, index) => (
            <li key={index} style={{ listStyleType: 'none', padding: '10px', borderBottom: '1px solid #ccc' }}>
              <h3>{result.restaurant_name} - {result.address}</h3>
              <p>Stars: {result.stars}</p>
              <p>Popularity (Review Count): {result.review_count}</p>
              <p>Sample User Review: {result.review_text || "No review available."}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
