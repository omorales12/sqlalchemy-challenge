# IMPORT DEPENDENCIES

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import pandas as pd
import datetime as dt

# CREATE ENGINE TO hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# REFLECT EXISTING DATABASE INTO NEW MODEL
Base = automap_base()

# REFLECT THE TABLES
Base.prepare(engine, reflect=True)

# SAVE REFERENCES TO EACH TABLE
Measurement = Base.classes.measurement
Station = Base.classes.station

# FLASK SETUP
app = Flask(__name__)

# HOME PAGE
@app.route("/")

def home():
    print("Server received a request for Home")
    return(
        f"Welcome to the weather API<br><br>"
        f"These are the available routes:<br>"
        f"/precipitation_analysis<br>"
        f"/station_analysis"
    )

# PRECIPITATION ANALYSIS
@app.route("/precipitation_analysis")

def precipitation_analysis():
    # Open session
    session = Session(engine)

    # Find the most recent date in the data set.
    most_recent = session.query(Measurement.date).order_by(Measurement.date.desc()).all()
    most_recent = most_recent[0][0]

    recent_year = int(most_recent[0:4])
    recent_month = int(most_recent[5:7])
    recent_day = int(most_recent[8:10])

    # Calculate the date one year from the last date in data set.
    start_date = dt.date(recent_year - 1, recent_month, recent_day)

    # Perform a query to retrieve the date and precipitation scores
    scores = session.query(Measurement.date, Measurement.prcp).where(Measurement.date >= start_date)

    # Close session
    session.close()

    # Save the query results as a Pandas DataFrame and set the index to the date column
    scores_df = pd.DataFrame(scores, columns=["Date", "Precipitation"])

    # Convert Pandas DF into a dictionary
    dictonary = []

    for index, row in scores_df.iterrows():
        dictionary1 = {}
        dictionary1[row["Date"]] = row["Precipitation"]
        dictonary.append(dictionary1)

    return jsonify(dictonary)


# STATION ANALYSIS
@app.route("/station_analysis")

def station_analysis():
    # Open session
    session = Session(engine)

    # Design a query to calculate the total number stations in the dataset
    stations = session.query(Station.station)
    num_stations = len(pd.DataFrame(stations))

    activity = session.query(Measurement.station)
    activity_df = pd.DataFrame(activity, columns=["Count"])
    activity_df = pd.DataFrame(activity_df["Count"].value_counts())
    activity_df.reset_index(inplace=True)

    # Convert Pandas DF into a dictionary
    dictonary = []

    for index, row in activity_df.iterrows():
        dictionary1 = {}
        dictionary1[row["index"]] = row["Count"]
        dictonary.append(dictionary1)

    return jsonify(dictonary)





if __name__ == '__main__':
    app.run(debug = True)
    
