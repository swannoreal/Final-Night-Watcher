from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pyAgrum as gum
import pyAgrum.lib.notebook as gnb
import pyAgrum.lib.explain as explain
#import pyAgrum.lib.bn_vs_bs as bnvsbn
from pylab import *
import matplotlib.pyplot as plt
import os

  
app = Flask(__name__)
#In my case, my React app was running on port 3001
CORS(app, resources={"/drinking-data": {"origins": "http://localhost:3001"}})
 

gum.about()
gnb.configuration()

#Defining the model structure

bn = gum.BayesNet('NW')

safe = bn.add(gum.LabelizedVariable('Safe', 'Safe', ['no', 'yes']))
alone = bn.add(gum.LabelizedVariable('Alone', 'Alone', ['no', 'yes']))
safety = bn.add(gum.LabelizedVariable('Safety', 'Safety', ['no', 'yes']))

fi = bn.add(gum.LabelizedVariable('Food_Intake', 'Food_Intake', ['no', 'yes']))
wi = bn.add(gum.LabelizedVariable('Water_Intake', 'Water_Intake', ['no', 'yes']))
fi_wi = bn.add(gum.LabelizedVariable('Food_And_Water_Intake', 'Food_And_Water_Intake', ['low', 'medium', 'high']))

age = bn.add(gum.LabelizedVariable('Age', 'Age', ['<21', '21-50', '50<']))
weight = bn.add(gum.LabelizedVariable('Weight', 'Weight', ['low', 'medium', 'high']))
gender = bn.add(gum.LabelizedVariable('Gender', 'Gender', ['male', 'female']))
bf = bn.add(gum.LabelizedVariable('Body_Fat', 'Body_Fat', ['low', 'medium', 'high']))
gpd = bn.add(gum.LabelizedVariable('GPD', 'GPD', ['no', 'yes']))
a_rc = bn.add(gum.LabelizedVariable('ARC', 'ARC', ['no', 'yes']))
prf = bn.add(gum.LabelizedVariable('Personal_Risk_Factors', 'Personal_Risk_Factors', ['low', 'high']))

units = bn.add(gum.LabelizedVariable('Units', 'Units', ['1-3', '4-10', 'above 11']))
duration = bn.add(gum.LabelizedVariable('Duration', 'Duration', ['>2 hours', '<2 hours']))
drf = bn.add(gum.LabelizedVariable('Drinking_Risk_Factors', 'Drinking_Risk_Factors', ['low', 'medium','high']))

physical = bn.add(gum.LabelizedVariable('Physical_Risk', 'Physical_Risk', ['low', 'medium', 'high']))
mental = bn.add(gum.LabelizedVariable('Mental_Risk', 'Mental_Risk', ['low', 'medium', 'high']))

#Arc creation according to defined dependencies (page 14 of the report)
for link in [(safe, safety), (alone, safety), (wi, fi_wi), (fi, fi_wi), (age, bf), (weight, bf), (gender, bf), (bf, prf), (gpd, a_rc), (a_rc, prf), (units, drf), (duration, drf), (safety, mental), (drf, mental), (drf, physical), (prf, physical), (fi_wi, physical)]:
  bn.addArc(*link)

#Uniform distribution for parent nodes
bn.cpt(safe).fillWith([0.5,0.5])
bn.cpt(alone).fillWith([0.5,0.5])
bn.cpt(fi).fillWith([0.5,0.5])
bn.cpt(wi).fillWith([0.5,0.5])
bn.cpt(age).fillWith([0.33,0.33,0.33])
bn.cpt(weight).fillWith([0.33,0.33,0.33])
bn.cpt(gender).fillWith([0.5,0.5])
bn.cpt(gpd).fillWith([0.5,0.5])
bn.cpt(units).fillWith([0.33,0.33,0.33])
bn.cpt(duration).fillWith([0.5,0.5])

#Safety node
bn.cpt(safety)[{'Safe':'yes', 'Alone':'yes'}] = [0.2, 0.8]
bn.cpt(safety)[{'Safe':'yes', 'Alone':'no'}] = [0,1]
bn.cpt(safety)[{'Safe':'no', 'Alone':'yes'}] = [1,0]
bn.cpt(safety)[{'Safe':'no', 'Alone':'no'}] = [0.5,0.5]

#Food and water mitigation
bn.cpt(fi_wi)[{'Food_Intake':'yes', 'Water_Intake':'yes'}] = [0.8,0.1,0.1]
bn.cpt(fi_wi)[{'Food_Intake':'yes', 'Water_Intake':'no'}] = [0.7,0.2,0.1]
bn.cpt(fi_wi)[{'Food_Intake':'no', 'Water_Intake':'yes'}] = [0.5,0.3,0.2]
bn.cpt(fi_wi)[{'Food_Intake':'no', 'Water_Intake':'no'}] = [0.3,0.4,0.3]

#ARC node
bn.cpt(a_rc)[{'GPD':'yes'}] = [0.4,0.6]
bn.cpt(a_rc)[{'GPD':'no'}] = [0.6,0.4]

#Body fat node
bn.cpt(bf)[{'Age':'<21', 'Weight':'low', 'Gender':'male'}] = [0.29,0.69,0.02]
bn.cpt(bf)[{'Age':'<21', 'Weight':'low', 'Gender':'female'}] = [0.39, 0.60, 0.01]
bn.cpt(bf)[{'Age':'<21', 'Weight':'medium', 'Gender':'male'}] = [0.01, 0.80, 0.19]
bn.cpt(bf)[{'Age':'<21', 'Weight':'medium', 'Gender':'female'}] = [0.01, 0.80, 0.19]
bn.cpt(bf)[{'Age':'<21', 'Weight':'high', 'Gender':'male'}] = [0.01, 0.71, 0.28]
bn.cpt(bf)[{'Age':'<21', 'Weight':'high', 'Gender':'female'}] = [0.01, 0.71, 0.28]

bn.cpt(bf)[{'Age':'21-50', 'Weight':'low', 'Gender':'male'}] = [0.01, 0.57, 0.42]
bn.cpt(bf)[{'Age':'21-50', 'Weight':'low', 'Gender':'female'}] = [0.01, 0.59, 0.40]
bn.cpt(bf)[{'Age':'21-50', 'Weight':'medium', 'Gender':'male'}] = [0.01, 0.47, 52]
bn.cpt(bf)[{'Age':'21-50', 'Weight':'medium', 'Gender':'female'}] = [0.01, 0.49, 0.50]
bn.cpt(bf)[{'Age':'21-50', 'Weight':'high', 'Gender':'male'}] = [0.01, 0.34, 0.65]
bn.cpt(bf)[{'Age':'21-50', 'Weight':'high', 'Gender':'female'}] = [0.01, 0.34, 0.65]

bn.cpt(bf)[{'Age':'50<', 'Weight':'low', 'Gender':'male'}] = [0.01, 0.59, 0.30]
bn.cpt(bf)[{'Age':'50<', 'Weight':'low', 'Gender':'female'}] = [0.01, 0.79, 0.20]
bn.cpt(bf)[{'Age':'50<', 'Weight':'medium', 'Gender':'male'}] = [0.01, 0.30, 0.69]
bn.cpt(bf)[{'Age':'50<', 'Weight':'medium', 'Gender':'female'}] = [0.01, 0.40, 0.59]
bn.cpt(bf)[{'Age':'50<', 'Weight':'high', 'Gender':'male'}] = [0.01, 0.19, 0.80]
bn.cpt(bf)[{'Age':'50<', 'Weight':'high', 'Gender':'female'}] = [0.01, 0.29, 0.70]

#Drinking related risk factors
bn.cpt(drf)[{'Units':'1-3', 'Duration':'<2 hours'}] = [0.8,0.1,0.1]
bn.cpt(drf)[{'Units':'1-3', 'Duration':'>2 hours'}] = [0.8,0.1,0.1]
bn.cpt(drf)[{'Units':'4-10', 'Duration':'<2 hours'}] = [0.3,0.4,0.3]
bn.cpt(drf)[{'Units':'4-10', 'Duration':'>2 hours'}] = [0.4,0.5,0.1]
bn.cpt(drf)[{'Units':'above 11', 'Duration':'<2 hours'}] = [0.1,0.1,0.8]
bn.cpt(drf)[{'Units':'above 11', 'Duration':'>2 hours'}] = [0.1,0.2,0.7]

#Personal risk factors
bn.cpt(prf)[{'ARC':'yes', 'Body_Fat':'low'}] = [0.65, 0.35]
bn.cpt(prf)[{'ARC':'yes', 'Body_Fat':'medium'}] = [0.55, 0.45]
bn.cpt(prf)[{'ARC':'yes', 'Body_Fat':'high'}] = [0.79, 0.21]
bn.cpt(prf)[{'ARC':'no', 'Body_Fat':'low'}] = [0.65, 0.35]
bn.cpt(prf)[{'ARC':'no', 'Body_Fat':'medium'}] = [0.99, 0.01]
bn.cpt(prf)[{'ARC':'no', 'Body_Fat':'high'}] = [0.80, 0.20]

#Physical risk
bn.cpt(physical)[{'Food_And_Water_Intake':'low', 'Drinking_Risk_Factors':'low', 'Personal_Risk_Factors':'low'}] = [0.40, 0.50, 0.10]
bn.cpt(physical)[{'Food_And_Water_Intake':'low', 'Drinking_Risk_Factors':'low', 'Personal_Risk_Factors':'high'}] = [0.35, 0.45, 0.20]
bn.cpt(physical)[{'Food_And_Water_Intake':'low', 'Drinking_Risk_Factors':'medium', 'Personal_Risk_Factors':'low'}] = [0.30, 0.40, 0.25]
bn.cpt(physical)[{'Food_And_Water_Intake':'low', 'Drinking_Risk_Factors':'medium', 'Personal_Risk_Factors':'high'}] = [0.25, 0.35, 0.40]
bn.cpt(physical)[{'Food_And_Water_Intake':'low', 'Drinking_Risk_Factors':'high', 'Personal_Risk_Factors':'low'}] = [0.10, 0.30,0.60]
bn.cpt(physical)[{'Food_And_Water_Intake':'low', 'Drinking_Risk_Factors':'high', 'Personal_Risk_Factors':'high'}] = [0.01, 0.05, 0.94]

bn.cpt(physical)[{'Food_And_Water_Intake':'medium', 'Drinking_Risk_Factors':'low', 'Personal_Risk_Factors':'low'}] = [0.50, 0.40, 0.10]
bn.cpt(physical)[{'Food_And_Water_Intake':'medium', 'Drinking_Risk_Factors':'low', 'Personal_Risk_Factors':'high'}] = [0.45, 0.35, 0.20]
bn.cpt(physical)[{'Food_And_Water_Intake':'medium', 'Drinking_Risk_Factors':'medium', 'Personal_Risk_Factors':'low'}] = [0.40, 0.30, 0.30]
bn.cpt(physical)[{'Food_And_Water_Intake':'medium', 'Drinking_Risk_Factors':'medium', 'Personal_Risk_Factors':'high'}] = [0.35, 0.25, 0.40]
bn.cpt(physical)[{'Food_And_Water_Intake':'medium', 'Drinking_Risk_Factors':'high', 'Personal_Risk_Factors':'low'}] = [0.30, 0.20, 0.50]
bn.cpt(physical)[{'Food_And_Water_Intake':'medium', 'Drinking_Risk_Factors':'high', 'Personal_Risk_Factors':'high'}] = [0.15, 0.15, 0.70]

bn.cpt(physical)[{'Food_And_Water_Intake':'high', 'Drinking_Risk_Factors':'low', 'Personal_Risk_Factors':'low'}] = [0.94, 0.05, 0.01]
bn.cpt(physical)[{'Food_And_Water_Intake':'high', 'Drinking_Risk_Factors':'low', 'Personal_Risk_Factors':'high'}] = [0.84, 0.10, 0.06]
bn.cpt(physical)[{'Food_And_Water_Intake':'high', 'Drinking_Risk_Factors':'medium', 'Personal_Risk_Factors':'low'}] = [0.74, 0.15, 0.11]
bn.cpt(physical)[{'Food_And_Water_Intake':'high', 'Drinking_Risk_Factors':'medium', 'Personal_Risk_Factors':'high'}] = [0.64, 0.20, 0.16]
bn.cpt(physical)[{'Food_And_Water_Intake':'high', 'Drinking_Risk_Factors':'high', 'Personal_Risk_Factors':'low'}] = [0.54, 0.25, 0.21]
bn.cpt(physical)[{'Food_And_Water_Intake':'high', 'Drinking_Risk_Factors':'high', 'Personal_Risk_Factors':'high'}] = [0.44, 0.30, 0.26]

#Mental risk
bn.cpt(mental)[{'Drinking_Risk_Factors':'low', 'Safety':'yes'}] = [0.75, 0.15, 0.10]
bn.cpt(mental)[{'Drinking_Risk_Factors':'low', 'Safety':'no'}] = [0.40, 0.30, 0.30]
bn.cpt(mental)[{'Drinking_Risk_Factors':'medium', 'Safety':'yes'}] = [0.55, 0.25, 0.20]
bn.cpt(mental)[{'Drinking_Risk_Factors':'medium', 'Safety':'no'}] = [0.30, 0.30, 0.40]
bn.cpt(mental)[{'Drinking_Risk_Factors':'high', 'Safety':'yes'}] = [0.30, 0.40, 0.30]
bn.cpt(mental)[{'Drinking_Risk_Factors':'high', 'Safety':'no'}] = [0.05, 0.15, 0.80]

ie = gum.LazyPropagation(bn)

# Route for seeing a data
@app.route('/drinking-data', methods=['POST'])
def get_data():
    drinkingData = request.json
    print("Received drinking data:", drinkingData)
    
    return jsonify({"message": "Data received successfully"})

    for var, value in drinkingData.items():
        ie.setEvidence({var: value})

    ie.makeInference()

    # Get the values of the probabilities of the 'physical' and 'mental' nodes to determine messages
    physical_prob = ie.posterior('Physical_Risk')
    mental_prob = ie.posterior('Mental_Risk')

    #Printing the different messages (page 24 of the report)
    #Additional messages (according to the user's age and alone/not alone)
    user_age = int(drinkingData.get('Age', 0))
    is_alone = drinkingData.get('Alone', 'no') == 'yes'

    physical_message = ""
    mental_message = ""

    # Determine the hierqrchies of posterior probabilites to select the state and consequently, the appropriate message
    #Mental risk
    if mental_prob[0] > mental_prob[1] and mental_prob[0] > mental_prob[2]:
        mental_message = "Low"
    elif mental_prob[1] > mental_prob[0] and mental_prob[1] > mental_prob[2]:
        mental_message = "Medium"
    else:
        mental_message = "High"
    #Physical risk
    if physical_prob[0] > physical_prob[1] and physical_prob[0] > physical_prob[2]:
        physical_message = "Low"
    elif physical_prob[1] > physical_prob[0] and physical_prob[1] > physical_prob[2]:
        physical_message = "Medium"
    else:
        physical_message = "High"

    # Display additional messages based on conditions
    if user_age < 18 and is_alone :
        additional_message = "You’re a little young to be out! You could give your parents a quick ring, they might be worried for you. \n Also, you should go find your friends or call someone, it’s always better to be accompanied."
    elif is_alone:
        additional_message = "You should go find your friends or call someone, it’s always better to be accompanied."
    elif user_age <18 :
        additional_message = "You’re a little young to be out! You could give your parents a quick ring, they might be worried for you."
    else:
        additional_message = ""

    # Construct final message based on mental and physical risk
    if mental_message == "Low":
        if physical_message == "Low":
            final_message = "You're off to a good start tonight. Keep an eye on your surroundings and remember to take regular breaks. \n Enjoy yourself responsibly and prioritize your well-being throughout the night."
        elif physical_message == "Medium":
            final_message = "Things are looking good mentally, but there's a bit of physical risk to consider. Stay cautious and aware of your surroundings. \n Take breaks when needed and ensure you're staying safe while having fun."
        else:  # High physical risk
            final_message = "While your mental state is stable, there's some notable physical risk tonight. Stay vigilant and prioritize your safety above all else. \n Don't hesitate to seek help or remove yourself from any risky situations."

    elif mental_message == "Medium":
        if physical_message == "Low":
            final_message = "You're doing alright mentally, but there's still some potential for physical challenges. Keep an eye on yourself and your surroundings. \n Take breaks as necessary and ensure you're staying safe throughout the night."
        elif physical_message == "Medium":
            final_message = "Things are a bit uncertain both mentally and physically. Stay cautious and mindful of your well-being. \n Take regular breaks, assess your surroundings, and don't hesitate to ask for help if needed."
        else:  # High physical risk
            final_message = "With some mental and physical uncertainties, it's important to prioritize your safety. Stay aware of your surroundings and trust your instincts. \n Consider seeking assistance or removing yourself from risky situations as needed."

    else:  # High mental risk
        if physical_message == "Low":
            final_message = "While your mental state may be challenging, physical risks are relatively low. Prioritize self-care and safety tonight. \n Stay vigilant and don't hesitate to seek help or take a break if needed."
        elif physical_message == "Medium":
            final_message = "With significant mental challenges and some physical risks, it's crucial to prioritize your well-being. Stay aware of your surroundings and listen to your body. \n Seek assistance or remove yourself from any risky situations as necessary."
        else:  # High physical risk
            final_message = "Tonight comes with significant challenges both mentally and physically. Prioritize your safety above all else. \n Stay vigilant, trust your instincts, and don't hesitate to seek help or remove yourself from any unsafe situations immediately."

    return jsonify({"final_message": final_message, "additional_message": additional_message})

if __name__ == '__main__':
    app.run(debug=True, port=8080)
