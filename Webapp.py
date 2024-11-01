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
    dates = get_dates_options()
    return render_template('data.html', group_options=groups, dates_options=dates)

@app.route('/credit')
def credit():
    return render_template('credit.html')
    


@app.route('/date')
def render_date():
    dates = get_dates_options()
    date = int(request.args.get('dates'))
    response = ofdate(date)
    dfact1 = "Highest Estimated Ammount of Deaths: " + str(response[0]["Highest Estimated Ammount of Deaths"])
    dfact2 = "Lowest Estimated Ammount of Deaths: " + str(response[0]["Lowest Estimated Ammount of Deaths"])
    return render_template('data.html', dates_options=dates, group_options=get_group_options(), dFact1=dfact1, dFact2=dfact2)

    
@app.route('/groups')    
def render_status():
    groups = get_group_options()
    group = request.args.get('group')
    status = decided(group)
    fact1 = "Confirmed Suicide: " + str(status[0]["Confirmed Suicide"]) 
    fact2 = "Possible Suicide: " + str(status[0]["Possible - Too Few Sources"])
    fact3 = "Highest Estimated Ammount of deaths: " + str(status[0]["Highest Estimated Ammount of deaths"])
    fact4 = "Lowest Estimated Ammount of deaths: " + str(status[0]["Lowest Estimated Ammount of deaths"])
    fact5 = "Ammount of Belt Bombs used: " + str(status[0]["Ammount of Belt Bombs used"])    
    fact6 = "Ammount of Truck Bombs used: " + str(status[0]["Ammount of Truck Bombs used"])
    fact7 = "Amount of Car Bombs used: " + str(status[0]["Amount of Car Bombs used"])
    fact8 = "Amount of Other Weapons used: " + str(status[0]["Amount of Other Weapons used"])
    fact10 = "Amount of Attackers: " + str(status[0]["Amount of Attackers"])
    return render_template('data.html', group_options=groups, date_options=get_dates_options(), Fact1=fact1, Fact2=fact2, Fact3=fact3, Fact4=fact4, Fact5=fact5, Fact6=fact6, Fact7=fact7, Fact8=fact8, Fact10=fact10)

    
def get_group_options():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('suicide_attacks.json') as suicide_data:
        groups = json.load(suicide_data)
    group=[]
    
    for g in groups:
        if g["groups"] not in group:
            group.append(g["groups"])
    
    return group
    
def decided(group):
    counts = {"Confirmed Suicide": 0, "Possible - Too Few Sources": 0, "Highest Estimated Ammount of deaths": 0, "Lowest Estimated Ammount of deaths": 0, "Ammount of Belt Bombs used": 0, "Ammount of Truck Bombs used": 0, "Amount of Car Bombs used": 0, "Amount of Other Weapons used": 0, "Amount of Unknown Weapons used": 0, "Amount of Attackers": 0, "Amount of Sources": 0}
    with open('suicide_attacks.json') as suicide_data:
        groups = json.load(suicide_data)
        for attack in groups: 
            if attack["groups"] == group:
                if attack["status"] == "Confirmed Suicide":
                    counts["Confirmed Suicide"] = counts["Confirmed Suicide"] + 1
                if attack["status"] == "Possible - Too Few Sources":
                    counts["Possible - Too Few Sources"] = counts["Possible - Too Few Sources"] + 1
                    attack["statistics"]["# killed_high"]
                counts["Highest Estimated Ammount of deaths"] = counts["Highest Estimated Ammount of deaths"] + attack["statistics"]["# killed_high"]
                attack["statistics"]["# killed_low"]
                counts["Lowest Estimated Ammount of deaths"] = counts["Lowest Estimated Ammount of deaths"] +  attack["statistics"]["# killed_low"]
                attack["statistics"]["# belt_bomb"]
                counts["Ammount of Belt Bombs used"] = counts["Ammount of Belt Bombs used"] + attack["statistics"]["# belt_bomb"]
                attack["statistics"]["# truck_bomb"]
                counts["Ammount of Truck Bombs used"] = counts["Ammount of Truck Bombs used"] + attack["statistics"]["# truck_bomb"]
                attack["statistics"]["# car_bomb"]
                counts["Amount of Car Bombs used"] = counts["Amount of Car Bombs used"] + attack["statistics"]["# car_bomb"] 
                attack["statistics"]["# weapon_oth"]
                counts["Amount of Other Weapons used"] = counts["Amount of Other Weapons used"] + attack["statistics"]["# weapon_oth"]
                attack["statistics"]["# attackers"]
                counts["Amount of Attackers"] = counts["Amount of Attackers"] + attack["statistics"]["# attackers"]  
    lal = [counts]
    return lal

def get_dates_options():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('suicide_attacks.json') as suicide_data:
        date = json.load(suicide_data)
    dates=[]
    
    for d in date:
        if d["date"]["year"] not in dates:
            dates.append(d["date"]["year"])
    print(dates)
    return dates
    
def ofdate(dates):
    counts = {"Highest Estimated Ammount of Deaths": 0, "Lowest Estimated Ammount of Deaths": 0}
    with open('suicide_attacks.json') as suicide_data:
        date = json.load(suicide_data)
        for time in date: 
            if time["date"]["year"] == dates:
                
                counts["Highest Estimated Ammount of Deaths"] = counts["Highest Estimated Ammount of Deaths"] + time["statistics"]["# killed_high"]
                
                counts["Lowest Estimated Ammount of Deaths"] = counts["Lowest Estimated Ammount of Deaths"] +  time["statistics"]["# killed_low"]

    lol = [counts]
    return lol

if __name__ == '__main__':
    app.run(debug=True) # change to False when running in production
