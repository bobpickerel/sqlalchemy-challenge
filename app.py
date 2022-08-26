from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

app = Flask(__name__)

# connect to the database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

Measure = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


@app.route("/")
def home():
    return (
            f"<h1>Welcome to the SQLALCHEMY MODULE 10 Challenge<br><h1>"
            f"<h2>Select available routes<br><h2>"
            f"/api/v1.0/precipitation<br>"
            f"/api/v1.0/stations<br>"
            f"/api/v1.0/tobs<br>"
            f"/api/v1.0/start/end<br>"
    )



@app.route("/api/v1.0/precipitation")
def precip():
    # return the previous year's precipitation as a json
    # Calculate the date one year from the last date in data set.
    firstDate = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    allData = session.query(Measure.date, Measure.prcp).filter(Measure.date > firstDate).all()
    session.close()
    #dictionary of the precipitation
    precipitation = {date: prcp for date, prcp in allData}
    #convert to a json
    return jsonify(precipitation) 


@app.route("/api/v1.0/stations")
def stations():
    #list of stations
    stationData = session.query(Station.station).all()
    session.close()

    stationList = list(np.ravel(stationData))

    return jsonify(stationList)


@app.route("/api/v1.0/tobs")
def tobs():
    firstDate = dt.date(2017,8,23) - dt.timedelta(days=365)
    #return previous year temperatures
    tempData = session.query(Measure.tobs).filter(Measure.station == 'USC00519281').\
                filter(Measure.date >= firstDate).all()
    session.close()

    tempList = list(np.ravel(tempData))

    return jsonify(tempList)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def dateStats(start=None, end=None):
    
    selection = [func.min(Measure.tobs), func.max(Measure.tobs), func.avg(Measure.tobs)]

    if not end:

        startDate = dt.datetime.strptime(start, "%m%d%Y")

        results = session.query(*selection).filter(Measure.date >= startDate).all()

        session.close()

        tempList = list(np.ravel(results))

        return jsonify(tempList)

    else:

        startDate = dt.datetime.strptime(start, "%m%d%Y")
        endDate = dt.datetime.strptime(end, "%m%d%Y")

        results = session.query(*selection).filter(Measure.date >= startDate).filter(Measure.date <= endDate).all()

        session.close()

        tempList = list(np.ravel(results))

        return jsonify(tempList)

  
    

    

if __name__ == "__main__":
    app.run(debug=True)

