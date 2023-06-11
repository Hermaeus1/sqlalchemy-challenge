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
start = automap_base()
# reflect the tables
start.prepare(engine,reflect=True)

# Save references to each table
measurements = start.classes.measurement
stations = start.classes.station

# Create our session (link) from Python to the DB
sesh = Session(engine)
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
    return ( 
        f"Precipitation: /Precipitation<br/>"
        f"Stations: /Stations<br/>"
        f"tobs: /Tobs<br/>"
        f"By Start Date: /[start_date format:yyyy-mm-dd]<br/>"
        f"By Start & End Date: /[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
    )

if __name__ == '__main__':
    app.run(debug=True)