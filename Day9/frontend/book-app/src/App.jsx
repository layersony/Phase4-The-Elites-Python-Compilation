import React, { useState } from 'react';
import LoginForm from './LoginForm';
import Dashboard from './Dashboard';

const App = () => {
  const [loggedIn, setLoggedIn] = useState(false);

  const handleLogin = () => {
    setLoggedIn(true);
  };

  const handleLogout = () => {
    setLoggedIn(false);
  };

  return (
    <div>
      {!loggedIn && <LoginForm onLogin={handleLogin} />}
      {loggedIn && <Dashboard onLogout={handleLogout} />}
    </div>
  );
};

export default App;
