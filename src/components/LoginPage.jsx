import React, { useState, setError } from 'react';
import { useNavigate } from 'react-router-dom';
import "./css/LoginPage.css";
import users from '../data/users.json'


function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  
  const navigate = useNavigate();

  const handleLogin = (e) => {
    
    e.preventDefault();
    const user = users.users.find((user) => user.email === email);
    if (user) {
      console.log(user)
      if (user.password === password){
        localStorage.setItem('loggedInUser', JSON.stringify({ email: user.email }));
        
        // Extract additional user information
        const { age, weight, gender, gpd } = user;

        // Store additional user information in another JSON file
        const userDataEntry = {
          email: user.email,
          age: age,
          weight: weight,
          gender: gender,
          gpd: gpd
        }

        // Add the user data entry to the existing user data JSON
        users.users.push(userDataEntry);

        // Update the user data JSON file
        // Note: This is a simplified approach, in a real-world application, you might use a backend server to handle this.
        localStorage.setItem('users', JSON.stringify(users));


        navigate('/home');
      } 
      else {
        setError('Incorrect Password');
      }
    } else {
      setError('Incorrect Email');
    }
    
  };

  return (
    
     <body>    
        <center> <h1> Welcome to Night Watcher! </h1> </center>   
            <form onSubmit={handleLogin}>  
                <center><div class="container">   
                    <label>Email : </label>   
                    <input type="email" placeholder="Enter Email" value={email} onChange={(e) => setEmail(e.target.value)} /> 
                    <label>Password : </label>  
                    <input type="password" placeholder="Enter Password" name="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                    <button id="loginButton" type="submit">Login</button>
                </div>
                </center> 
                
                  
                         
            </form>     
    </body>  
      
      
  );
}

export default LoginPage;
