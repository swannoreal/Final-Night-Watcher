import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { useHistory } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import HomePage from './components/HomePage';
import DrinkingPage from './components/DrinkingPage';


function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path="/" exact component={LoginPage} />
          <Route path="/home" component={HomePage} />
          <Route path="/drinking" component={DrinkingPage} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
