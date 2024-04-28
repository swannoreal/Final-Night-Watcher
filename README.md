The App Night Watcher has four different oages that the user can acces: 

- the login page (LoginPage.jsx) that is the default page that user access. The page collects the user's email and password, checking if they correspond to existing information in the temporary database "users.json". Once the user is logged in, they access:
- the home page (HomePage.jsx). The user can either logout, being routed back ot the login page, or click on a button to fill out:
- a questionnaire to share their current situation on a night out (DrinkingPage.jsx). The information input is sent to: 
- a Python API (bn.py), where an inference engine is started. The user's information is fed to a prediction model running on the Bayesian Network present in the API, and the posterior probabilities of the "Mental Risk" and "Physical Risk" nodes are collected and sent back to:
- the prediction display page "Prediction.jsx". A specific message is displayed to the user, recommending the best course of action according to the prediction of model.

Each page has CSS files linked to them (with their respective names)