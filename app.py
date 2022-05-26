# <!-- ### Part 2: Design Your Climate App

# Now that you have completed your initial analysis, you’ll design a Flask API based on the queries that you have just developed.

# Use Flask to create your routes, as follows:

# * `/`

#     * Homepage.

#     * List all available routes.

# * `/api/v1.0/precipitation`

#     * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

#     * Return the JSON representation of your dictionary.

# * `/api/v1.0/stations`

#     * Return a JSON list of stations from the dataset.

# * `/api/v1.0/tobs`

#     * Query the dates and temperature observations of the most active station for the previous year of data.

#     * Return a JSON list of temperature observations (TOBS) for the previous year.

# * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

#     * Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range.

#     * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than or equal to the start date.

#     * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates from the start date through the end date (inclusive). -->

from flask import Flask, jsonify

# Import data
from Notebook.ipynb import *

app = Flask(__name__)

@app.route("/")
    def home_page
        return (
            f"/api/v1.0/precipitation"
            f"/api/v1.0/stations"
            f"/api/v1.0/tobs"
            f"/api/v1.0/<start>"
        )

@app.route("/api/v1.0/precipitation")
    #     * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
    #     * Return the JSON representation of your dictionary.
    def precipitation()
        measurements = session.query(Measurement)
        most_recent_date = measurements[-1].date
        previous_year = datetime.fromisoformat(most_recent_date) - relativedelta(years=1)
                                            
        measurements = session.query(Measurement).\
            filter(Measurement.date >= previous_year).\
            group_by(Measurement.date).\
            order_by(Measurement.date).all()
        df = pd.DataFrame(columns = ["Date", "PRCP"])
        for measurement in measurements:
            df = df.append({'Date' : measurement.date, 'PRCP' : measurement.prcp}, ignore_index=True)

        results_pairs = {}
        for a, b in x, y:
            results_pairs.append({a: b})
        return jsonify(results_pairs)


@app.route("/api/v1.0/stations")
    def stations
        stations = session.query(Measurement.station, func.count(Measurement.station)).\
                group_by(Measurement.station).\
                order_by(func.count(Measurement.station).desc()).all()
        return stations

@app.route("/api/v1.0/tobs")
    def tobs
        stations = session.query(Measurement.station, func.count(Measurement.station)).\
            filter(Measurement.date >= previous_year).\
            group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).all()
            
        top_station = stations[0][0]

        top_measurements = session.query(Measurement).\
            filter(Measurement.date >= previous_year).\
            filter(Measurement.station == top_station).\
            group_by(Measurement.date).\
            order_by(Measurement.date).all()
            
        return top_measurements

@app.route("/api/v1.0/<start>")
    def calculate_start(start_date)
        measurements = session.query(Measurement).\
            filter(Measurement.date >= start_date).\
            group_by(Measurement.date).\
            order_by(Measurement.date).all()

        max_temp = session.query(Measurement.station, func.max(Measurement.prcp)).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.station == top_station).all()
        max_temp_value = max_temp[0][1]
        print("Max Temperature is " + str(max_temp_value))

        min_temp = session.query(Measurement.station, func.min(Measurement.prcp)).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.station == top_station).all()
        min_temp_value = min_temp[0][1]
        print("Min Temperature is " + str(min_temp_value))

        average_temp = session.query(Measurement.station, func.avg(Measurement.prcp)).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.station == top_station).all()
        avg_temp_value = average_temp[0][1]
        print("Average Temperature is " + str(avg_temp_value))
        return jsonify(max_temp_value, min_temp_value, avg_temp_value)

@app.route("/api/v1.0/<start>/<end>")
    def calculate_start_end(start_date, end_date)
        max_temp = session.query(Measurement.station, func.max(Measurement.prcp)).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.date =< end_date).all()
        max_temp_value = max_temp[0][1]
        print("Max Temperature is " + str(max_temp_value))

        min_temp = session.query(Measurement.station, func.min(Measurement.prcp)).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.date =< end_date).all()
        min_temp_value = min_temp[0][1]
        print("Min Temperature is " + str(min_temp_value))

        average_temp = session.query(Measurement.station, func.avg(Measurement.prcp)).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.date =< end_date).all()
        avg_temp_value = average_temp[0][1]
        print("Average Temperature is " + str(avg_temp_value))
        return jsonify(max_temp_value, min_temp_value, avg_temp_value)