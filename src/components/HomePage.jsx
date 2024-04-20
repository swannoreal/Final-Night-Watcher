import React from 'react';
import { useHistory } from 'react-router-dom';

function HomePage() {
  const history = useHistory();

  const handleLogout = () => {
    // Perform logout logic here
    history.push('/');
  };

  const handleDrinkingPage = () => {
    history.push('/drinking');
  };

  return (
    <div>
      <h2>Hello, [Name of User]</h2>
      <button onClick={handleLogout}>Logout</button>
      <button onClick={handleDrinkingPage}>I'm out drinking tonight</button>
    </div>
  );
}

export default HomePage;
