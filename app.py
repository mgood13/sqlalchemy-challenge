import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

app = Flask(__name__)
session = Session(engine)

Measurement = Base.classes.measurement
Station = Base.classes.station
# Extract the last row from our data
lastrow = engine.execute('SELECT * FROM measurement WHERE id=(SELECT max(id) FROM measurement)').fetchall()

# Convert the date into a datetime object
lastdate = dt.datetime.strptime(lastrow[0][2],'%Y-%m-%d')

# Generate our data from one year prior to the last data in our table
# 52 weeks is typically considered a year but that's actually only 364 days
yearago = lastdate - dt.timedelta(days = 1, weeks = 52)


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"/api/v1.0/stations<br/>"
        "<br/>"
        "Start and End in the above routes represent start and end dates <br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    measurement_df = pd.DataFrame(session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > yearago).all())
    measurement_df = measurement_df.dropna()
    measurement_df = measurement_df.set_index('date')
    measurement_dict = measurement_df.to_dict()
    return jsonify(measurement_dict['prcp'])


@app.route("/api/v1.0/stations")
def stations():
    stationlist = engine.execute('select * from station').fetchall()
    stations = []
    for station in stationlist:
        stations.append(station[2])
    return jsonify(stations)







if __name__ == '__main__':
    app.run(debug=True)
