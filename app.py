# Import all the dependencies
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

# Create the engine and map the base
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()

# Reflect the base to get our table representations
Base.prepare(engine, reflect=True)

#Initialize our flask app and our engine
app = Flask(__name__)
session = Session(engine)

# Create our representations of the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Extract the last row from our data
lastrow = engine.execute('SELECT * FROM measurement WHERE id=(SELECT max(id) FROM measurement)').fetchall()

# Convert the date into a datetime object
lastdate = dt.datetime.strptime(lastrow[0][2],'%Y-%m-%d')

# Generate our data from one year prior to the last data in our table
# 52 weeks is typically considered a year but that's actually only 364 days
yearago = lastdate - dt.timedelta(days = 1, weeks = 52)

# Bring over the function from the original file that returns the minimum, average, and maximum temperatures over a given range
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.

    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d

    Returns:
        TMIN, TAVE, and TMAX
    """

    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)). \
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

# This route explains and displays to the user all the available route options
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        "<br/>"
        f"The Precipitation Module returns all of the precipitation values along with their recorded dates <br/>"
        f"Route: /api/v1.0/precipitation<br/>"
        "<br/>"
        f"The Stations Module returns the names of all of the stations available in our dataset <br/>"
        f"/api/v1.0/stations<br/>"
        "<br/>"
        f"The following date module returns a list of the Minimum, Average, and Maximum Temperatures recorded over the given date range <br/>"
        f"If no end date is given the end date is assumed to be the last datapoint available in the dataset. <br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        "<br/>"
        "*Start and End in the above routes represent start and end dates* <br/>"
    )

# This app returns a dictionary of all of the precipitation data available in our dataset
# (with the rows with N/A values dropped)
@app.route("/api/v1.0/precipitation")
def precipitation():
    measurement_df = pd.DataFrame(session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > yearago).all())
    measurement_df = measurement_df.dropna()
    measurement_df = measurement_df.set_index('date')
    measurement_dict = measurement_df.to_dict()
    return jsonify(measurement_dict['prcp'])


# This app returns the names of all available stations
@app.route("/api/v1.0/stations")
def stations():
    stationlist = engine.execute('select * from station').fetchall()
    stations = []
    for station in stationlist:
        stations.append(station[2])
    return jsonify(stations)


# This app returns all the temperature observations of our most active station
@app.route("/api/v1.0/tobs")
def tobs():
    lastyear_df = pd.DataFrame(
        session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.date > yearago).all())
    stationcount = lastyear_df.groupby('station').count()
    activestation = stationcount[stationcount.date == stationcount.date.max()].reset_index()['station'].to_string()
    activestation = activestation[5:]
    smaller_df = lastyear_df.loc[lastyear_df['station'] == activestation, :]
    return jsonify(smaller_df['tobs'].tolist())


# This route takes user input for start and end dates and returns the minimum, maximum, and average temperatures
# If no end date is given the final datapoint in the dataset is given as the end date
@app.route("/api/v1.0/<start>", defaults={'end':None})
@app.route("/api/v1.0/<start>/<end>")
def normal(start,end):
    startdate = start
    if end == None:
        enddate = lastrow[0][2]
    else:
        enddate = end

    return jsonify(calc_temps(startdate,enddate)[0])



if __name__ == '__main__':
    app.run(debug=True)
