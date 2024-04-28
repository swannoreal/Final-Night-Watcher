import React, {useState, useEffect} from 'react';
import { useNavigate } from 'react-router-dom';
import users from '../data/users.json'
import "./css/HomePage.css"

function HomePage() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));
  
    if (loggedInUser) {
      const foundUser = users.users.find(user => user.email === loggedInUser.email);
      
      if (foundUser) {
        setUser(foundUser);
      }
    }
  }, []);
  

  const handleLogout = () => {
    navigate('/');
  };

  const handleDrinkingPage = () => {
    //console.log("Hello");
    navigate('/drinking');
  };

  return (
    <body>
        <center><div class="homeContainer">
        <h2 id="welcomeMessage">Hello, {user && user.name}</h2>
        <button id="logoutButton" onClick={handleLogout}>Logout</button>
        <button id="sessionButton" onClick={handleDrinkingPage}>I'm out drinking tonight!</button>
        </div>
        </center>
    </body>
    
  );
}

export default HomePage;
