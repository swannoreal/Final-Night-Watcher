import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import "./css/Prediction.css"

function Prediction() {
  const [predictionData, setPredictionData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8080/drinking-data');
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        const data = await response.json();
        setPredictionData(data);
        setLoading(false);
      } catch (error) {
        setError(error.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <center><h1>What we suggest:</h1></center>
      <div>
        <center><p>{predictionData.final_message}</p></center>
        {predictionData.additional_message && (
          <p>{predictionData.additional_message}</p>
        )}
      </div>
    </div>
  );
}

export default Prediction;
