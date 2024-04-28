// DrinkingPage.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import "./css/DrinkingPage.css"
import users from '../data/users.json'

function DrinkingPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [drinkingData, setDrinkingData] = ('')
  const [alone, setAlone] = useState(false);
  const [safe, setSafe] = useState(false);
  const [typeOfDrink, setTypeOfDrink] = useState('');
  const [units, setUnits] = useState(0);
  const [duration, setDuration] = useState(false);
  const [food, setFood] = useState(false);
  const [water, setWater] = useState(false);
  const navigate = useNavigate();

  const user = users.users.find((user) => user.email === email);

  const handleSubmit = () => {

    if (user) {
      console.log(user)
      if (user.password === password){
        localStorage.setItem('loggedInUser', JSON.stringify({ email: user.email }));
        
      }
      //Information sent to the BN residing in the API
      const { age, weight, gender, gpd } = user;
      const drinkingData = {
      alone: alone,
      safe: safe,
      typeOfDrink: typeOfDrink,
      units: units,
      duration: duration,
      food: food,
      water: water,
      age: age,
      weight: weight,
      gender: gender,
      gpd: gpd
    }
    };
  
    //in my case, my Prediction model API was running on port 8080
    fetch('http://localhost:8080/drinking-data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({drinkingData}),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(drinkingData => {
        console.log('Success:', drinkingData);
      })
      .catch(error => {
        console.error('Error:', error);
      });
      navigate('/prediction')
  };

  return (
    <body>
        <div>
            <div class="drinkingContainer">
            <center><h2>How is your night going?</h2></center>
              <div class="question">
                <label>
                Are you alone?
                <input type="radio" value="yes" name="alone" onChange={() => setAlone(true)} /> Yes
                <input type="radio" value="no" name="alone" onChange={() => setAlone(false)} /> No
                </label>
            </div>
            <div class="question">
                <label>
                Do you feel safe?
                <input type="radio" value="yes" name="safe" onChange={() => setSafe(true)} /> Yes
                <input type="radio" value="no" name="safe" onChange={() => setSafe(false)} /> No
                </label>
            </div>
            <div class="question">
                <label>
                What are you drinking?
                <input type="text" value={typeOfDrink} onChange={(e) => setTypeOfDrink(e.target.value)} />
                </label>
            </div>
            <div class="question">
                <label>
                How many drinks have you had?
                <input type="range" min="0" max="11" step="1" id="rangeInput" value={units} onChange={(e) => setUnits(e.target.value)} />
                <p id="rangeValue">Value: </p>
                </label>
            </div>
            <div class="question">
                <label>
                How long have you been drinking?
                <input type="radio" value="over two hours" name="duration" onChange={() => setDuration(true)} /> Over 2 hours
                <input type="radio" value="under two hours" name="duration" onChange={() => setDuration(false)} /> Under 2 hours
                </label>
            </div>
            <div class="question">
                <label>
                Have you had food today?
                <input type="radio" value="yes" name="food" onChange={() => setFood(true)} /> Yes
                <input type="radio" value="no" name="food" onChange={() => setFood(false)} /> No
                </label>
            </div>
            <div class="question">
                <label>
                Have you had water today?
                <input type="radio" value="yes" name="water" onChange={() => setWater(true)} /> Yes
                <input type="radio" value="no" name="water" onChange={() => setWater(false)} /> No
                </label>
            </div>
            <center><button id="drinkingButton" onClick={handleSubmit}>Submit</button></center>
            </div>
        
        </div>
    </body>
  );
}

export default DrinkingPage;
