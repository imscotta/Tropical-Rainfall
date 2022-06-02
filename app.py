# <!-- ### Part 2: Design Your Climate App

from flask import Flask, jsonify

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from sqlalchemy import distinct
import pandas as pd

import matplotlib
from matplotlib import style
import matplotlib.pyplot as plt
import pandas as pd

# Select only the date and prcp values.
from datetime import datetime
from dateutil. relativedelta import relativedelta
import numpy as np

# Create engine using the database file
engine = create_engine(f"sqlite:////Users/swa/Documents/UC_Irvine/Homework/10-Advanced-Data-Storage-and-Retrieval/Instructions/Resources/hawaii.sqlite") 
conn = engine.connect()

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Print all of the classes mapped to the Base
Base.classes.keys()

# Assign the classes to variables called Station and Measurement
Station = Base.classes.station
Measurement = Base.classes.measurement

app = Flask(__name__)

# * `/`
#     * Homepage.
#     * List all available routes.

@app.route("/")
def homepage():
    return (
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start<br>"
        f"/api/v1.0/start/end"
    )

# * `/api/v1.0/precipitation`
#     * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
#     * Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create a session
    session = Session(engine)

    measurements = session.query(Measurement)
    most_recent_date = measurements[-1].date
    previous_year = datetime.fromisoformat(most_recent_date) - relativedelta(years=1)
                                        
    measurements = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= previous_year).\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()

    session.close()

    results_pairs = {date: prcp for date, prcp in measurements}

    return jsonify(results_pairs)

# * `/api/v1.0/stations`
#     * Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    # Create a session
    session = Session(engine)

    stations = session.query(Measurement.station, func.count(Measurement.station)).\
            group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).all()

    session.close()
    
    stations = list(np.ravel(stations))

    return jsonify(stations)

# * `/api/v1.0/tobs`
#     * Query the dates and temperature observations of the most active station for the previous year of data.
#     * Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    # Create a session
    session = Session(engine)

    # Find the most recent date in the dataset.
    # Using this date, retrieve the previous 12 months of precipitation data by querying the 12 previous months of data. Note: Do not pass in the date as a variable to your query.
    measurements = session.query(Measurement)
    most_recent_date = measurements[-1].date
    previous_year = datetime.fromisoformat(most_recent_date) - relativedelta(years=1)

    stations = session.query(Measurement.station, func.count(Measurement.station)).\
        filter(Measurement.date >= previous_year).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()

    top_station = stations[0][0]

    top_measurements = session.query(Measurement).\
        filter(Measurement.date >= previous_year).\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()

    session.close()

    df = pd.DataFrame(columns = ["Date", "PRCP"])
    for measurement in top_measurements:
        df = df.append({'TOBS' : measurement.tobs}, ignore_index=True)

    x = np.array(df["TOBS"].values)

    top_measurements = list(np.ravel(x))

    return jsonify(top_measurements)

# * `/api/v1.0/<start>`
#     * Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range.\
#     * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than or equal to the start date.
#     * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates from the start date through the end date (inclusive).

@app.route("/api/v1.0/")
def calculate_start(start_date):
    # Create a session
    session = Session(engine)

    max_temp = session.query(Measurement.station, func.max(Measurement.prcp)).\
        filter(Measurement.date >= start_date).all()
    max_temp_value = max_temp[0][1]
    print("Max Temperature is " + str(max_temp_value))

    min_temp = session.query(Measurement.station, func.min(Measurement.prcp)).\
        filter(Measurement.date >= start_date).all()
    min_temp_value = min_temp[0][1]
    print("Min Temperature is " + str(min_temp_value))

    average_temp = session.query(Measurement.station, func.avg(Measurement.prcp)).\
        filter(Measurement.date >= start_date).all()
    avg_temp_value = average_temp[0][1]
    print("Average Temperature is " + str(avg_temp_value))

    session.close()

    return jsonify(max_temp_value, min_temp_value, avg_temp_value)

# * `/api/v1.0/<start>/<end>`
#     * Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range.\
#     * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than or equal to the start date.
#     * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates from the start date through the end date (inclusive).

@app.route("/api/v1.0/<start>/<end>")
def calculate_start_end(start_date, end_date):
    # Create a session
    session = Session(engine)

    max_temp = session.query(Measurement.station, func.max(Measurement.prcp)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()
    max_temp_value = max_temp[0][1]
    print("Max Temperature is " + str(max_temp_value))

    min_temp = session.query(Measurement.station, func.min(Measurement.prcp)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()
    min_temp_value = min_temp[0][1]
    print("Min Temperature is " + str(min_temp_value))

    average_temp = session.query(Measurement.station, func.avg(Measurement.prcp)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()
    avg_temp_value = average_temp[0][1]
    print("Average Temperature is " + str(avg_temp_value))

    session.close()

    return jsonify(max_temp_value, min_temp_value, avg_temp_value)

if __name__ == "__main__":
    app.run(debug=True)