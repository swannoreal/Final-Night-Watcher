// DrinkingPage.js
import React, { useState } from 'react';

function DrinkingPage() {
  const [alone, setAlone] = useState(false);
  const [safe, setSafe] = useState(false);
  const [typeOfDrink, setTypeOfDrink] = useState('');
  const [units, setUnits] = useState(0);
  const [duration, setDuration] = useState(false);
  const [food, setFood] = useState(false);
  const [water, setWater] = useState(false);

  const handleSubmit = () => {
    // Compile variables and their values into a JSON file
    const drinkingData = {
      Alone: alone,
      Safe: safe,
      Type_Of_Drink: typeOfDrink === 'beer' || typeOfDrink === 'cider' ? 2.05 : typeOfDrink === 'wine' ? 2.3 : 3,
      Units: units,
      Duration: duration,
      fi: food,
      wi: water,
    };

    console.log(drinkingData);
    // Submit logic
  };

  return (
    <div>
      <h2>Drinking Questions</h2>
      <div>
        <label>
          Are you alone?
          <input type="radio" value="yes" name="alone" onChange={() => setAlone(true)} /> Yes
          <input type="radio" value="no" name="alone" onChange={() => setAlone(false)} /> No
        </label>
      </div>
      <div>
        <label>
          Do you feel safe?
          <input type="radio" value="yes" name="safe" onChange={() => setSafe(true)} /> Yes
          <input type="radio" value="no" name="safe" onChange={() => setSafe(false)} /> No
        </label>
      </div>
      <div>
        <label>
          What are you drinking?
          <input type="text" value={typeOfDrink} onChange={(e) => setTypeOfDrink(e.target.value)} />
        </label>
      </div>
      <div>
        <label>
          How many drinks have you had?
          <input type="range" min="1" max="10" value={units} onChange={(e) => setUnits(e.target.value)} />
        </label>
      </div>
      <div>
        <label>
          How long have you been drinking?
          <input type="radio" value="over two hours" name="duration" onChange={() => setDuration(true)} /> Over two hours
          <input type="radio" value="under two hours" name="duration" onChange={() => setDuration(false)} /> Under two hours
        </label>
      </div>
      <div>
        <label>
          Have you had food today?
          <input type="radio" value="yes" name="food" onChange={() => setFood(true)} /> Yes
          <input type="radio" value="no" name="food" onChange={() => setFood(false)} /> No
        </label>
      </div>
      <div>
        <label>
          Have you had water today?
          <input type="radio" value="yes" name="water" onChange={() => setWater(true)} /> Yes
          <input type="radio" value="no" name="water" onChange={() => setWater(false)} /> No
        </label>
      </div>
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}

export default DrinkingPage;
