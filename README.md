This fikle contains code for the ~Night Watcher frontend and its Flask API backend (prediction model). Follow the instructions below to set up and run the application:

Installation


1. Backend (Flask API)
Navigate to the backend directory:
cd backend
Create a virtual environment (optional but recommended) use python3 if on Mac and if Python 3 is installed:
python -m venv venv 
Install dependencies using pip:
pip intsall pyagrum
pip instal Flask-SQLAlchemy
Run the api:
python prediction_model.py


2. Frontend (React.js)
Navigate to the frontend directory:
cd components
Start the development server:
npm start
Open your browser and navigate to http://localhost:3000 (in mycase, port 3001) to view the application.


The App Night Watcher has four different oages that the user can acces: 

- the login page (LoginPage.jsx) that is the default page that user access. The page collects the user's email and password, checking if they correspond to existing information in the temporary database "users.json". Once the user is logged in, they access:
- the home page (HomePage.jsx). The user can either logout, being routed back ot the login page, or click on a button to fill out:
- a questionnaire to share their current situation on a night out (DrinkingPage.jsx). The information input is sent to: 
- a Python API (bn.py), where an inference engine is started. The user's information is fed to a prediction model running on the Bayesian Network present in the API, and the posterior probabilities of the "Mental Risk" and "Physical Risk" nodes are collected and sent back to:
- the prediction display page "Prediction.jsx". A specific message is displayed to the user, recommending the best course of action according to the prediction of model.

Each page has CSS files linked to them (with their respective names)