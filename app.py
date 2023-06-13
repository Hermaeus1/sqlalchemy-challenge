# Import the dependencies.
import numpy as np
from pathlib import Path
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Start = automap_base()
# reflect the tables
Start.prepare(autoload_with=engine,reflect=True)

# Save references to each table
Measurement = Start.classes.measurement
Station = Start.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    print("Loading routes list")
    #list of routes
    return ( 
        f"welcome to Hawaii"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"tobs: /api/v1.0/tobs<br/>"
        f"Start Date: /api/v1.0/<start><br/>"
        f"Custom Date: /api/v1.0/<start>/<end><br/>"
        f"Pass dates as MMDDYYYY"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    Date = dt.date(2017,8,23)-dt.timedelta(days=365)

    #grab precip data using the date from climate starter
    precip_results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= Date).all()
    session.close()

    #empty list to jsonify
    dripdrop = []
    for date,prcp in precip_results:
        #init dict
        prcp_dict = {}
        #smack in the two pieces
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        dripdrop.append(prcp_dict)

    return jsonify(precip_results)

@app.route("/api/v1.0/stations")
def places():

    #grab station data
    station_results = session.query(Station.station).order_by(Station.station).all()
    session.close()
    stationsss = list(np.ravel(station_results))
    
    return jsonify(stationsss)

@app.route("/api/v1.0/tobs")
def tobs():
   
    Date = dt.date(2017,8,23)-dt.timedelta(days=365)
    #grab tobs data

    #grab all the results then filter to capture the most recent for the most active station
    tobs_results = session.query(Measurement.tobs).filter(Measurement.date >= Date).\
    filter(Measurement.station == 'USC00519281').all()
    sesh.close()
    #make list
    tobsList = list(np.ravel(tobs_results))
    #give list
    return jsonify(tobsList)

@app.route("/api/v1.0/temp/<start>")
def starts(start=None):
    """Return TMIN, TAVG, TMAX."""

    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    start = dt.datetime.strptime(start, "%m%d%Y")
    results = session.query(*sel).\
        filter(Measurement.date >= start).all()

    session.close()
    #Convert to a list
    temps = list(np.ravel(results))
    #return the temperatures
    return jsonify(temps)
   


@app.route("/api/v1.0/temp/<start>/<end>")
def startsNends(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""

    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # calculate TMIN, TAVG, TMAX with start and stop
    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

if __name__ == '__main__':
    app.run(debug=True)