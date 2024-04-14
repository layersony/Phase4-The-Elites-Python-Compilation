import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = ({ onLogout }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [data, setData] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:8081/user', { headers: { Authorization: `Bearer ${token}` } });
        setData(response.data.message);
        setLoading(false);
      } catch (error) {
        setError('Unauthorized');
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    onLogout();
  };

  return (
    <div>
      <h2>Dashboard</h2>
      {loading && <p>Loading...</p>}
      {error && <p>{error}</p>}
      {data && <p>{data}</p>}
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default Dashboard;
