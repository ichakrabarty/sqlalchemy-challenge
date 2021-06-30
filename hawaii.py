import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Here are the available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    prec_data = []
    for result in results:
        prec_dict = {}
        prec_dict['date'] = result.date
        prec_dict['prcp'] = result.prcp
        prec_data.append(prec_dict)
    return jsonify(prec_data)  

@app.route("/api/v1.0/stations")    
def station():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    most_active_station = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519397').all()
    session.close()  

    most_active_station_list = list(most_active_station)   

    return jsonify(most_active_station_list)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    start_date = session.query(Measurement.date, func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    session.close() 

    start_date_list = list(start_date)

    return jsonify(start_date_list)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    session = Session(engine)
    start_end_date = session.query(Measurement.date, func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    session.close() 

    start_end_date_list = list(start_end_date)

    return jsonify(start_end_date_list)

if __name__ == "__main__":
    app.run(debug=True)      

