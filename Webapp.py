from flask import Flask, request, render_template, flash
from markupsafe import Markup

import os
import json

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/data')
def data():
    groups = get_group_options()
    return render_template('data.html', group_options=groups)

@app.route('/credit')
def credit():
    return render_template('credit.html')
    
    
@app.route('/groups')    
def render_status():
    groups = get_group_options()
    group = request.args.get('group')
    status = status_decided(group)
    fact1 = "Confirmed Suicide: " + str(status[0])
    fact2 = "Possible Suicide: " + str(status[0])
    fact3 = "Highest Estimated Ammount of deaths: " + str(status[0])
    return render_template('data.html', group_options=groups, Fact1=fact1, Fact2=fact2, Fact3=fact3)

    
def get_group_options():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('suicide_attacks.json') as suicide_data:
        groups = json.load(suicide_data)
    group=[]
    
    for g in groups:
        if g["groups"] not in group:
            group.append(g["groups"])
    
    return group
    
def status_decided(group):
    numbers = []
    counts = {}
    for num in numbers:
            if num in counts:
                counts[Confirmed] = counts[Confirmed] + 1
            else:
                counts[Possible] = 1
    lal = [numbers, counts]
    return lal





if __name__ == '__main__':
    app.run(debug=True) # change to False when running in production