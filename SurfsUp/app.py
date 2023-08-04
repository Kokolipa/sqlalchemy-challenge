#Hello - This will be the main header - section of comments - HEADING comments 
# * Theses type of comments will be commented out to outline my thoughts - WALKTHROUGH comments
# ? Theses type of comments will be commented out to clarify complex code - CLARIFICATION comments
# ! This type of comments will be used to update/fix my code/improve it for next time - ACTION/IMPROVEMENT comments
# todo - These type of comments will be used to outline new trick/function process- FLOW/HOW? comments
    # todo --> Example: Creating a pivot table with pandas -- Include the following arguments: [index = , columns = , values = ,aggfunc = , margins = ]

# * Import Numpy & Datetime
import numpy as np
import datetime as dt

# * Import SQLalchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

# * Import Flask
from flask import Flask, jsonify

# * Database Setup
#* ----------------------------------------------------------------------------
path = "/Users/galbeeir/Desktop/git/sqlalchemy_challenge/Starter_Code/SurfsUp/Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{path}")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station


# * Flask Setup
# * ----------------------------------------------------------------------------
app = Flask(__name__)

################################################################
# *Flask Routes
# * ----------------------------------------------------------------------------
################################################################

# ? ROUTE SOURCE - Homepage
#?----------------------------------------------------------------
@app.route("/") 
@app.route('/home')
def homepage():
    # * Listing avaiable API roots
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>" 
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start/end<br/>" 
    )


# ? ROUTE SOURCE - precipitation
#?----------------------------------------------------------------
@app.route('/api/v1.0/precipitation')
def precipitation():
    # TODO: Open session
    session = Session(engine)

    results = session.query(measurement.date, measurement.prcp).all()
    
    # TODO: Close session
    session.close()

    precipitation_inclusive = []

    for date, prcp in results:
        dictionary = {}
        dictionary[date] = prcp

        precipitation_inclusive.append(dictionary)
    
    return jsonify(precipitation_inclusive)


# ? ROUTE SOURCE - stations
#?----------------------------------------------------------------
@app.route('/api/v1.0/stations')
def stations():
    # TODO: Open session
    session = Session(engine)

    results = session.query(station.station).all()
    
    # TODO: Close session
    session.close()

    return jsonify(list(np.ravel(results)))


# ? ROUTE SOURCE - tobs
#?----------------------------------------------------------------
@app.route('/api/v1.0/tobs')
def tobs():
    # TODO: Open session
    session = Session(engine)

    most_active_stations = (session
                            .query(measurement.station, func.count(measurement.station).label('count'))
                            .group_by(measurement.station)
                            .order_by(desc('count'))
                            .all())
    station_last_date = (session.query(func.max(measurement.date))
                         .filter(measurement.station == most_active_stations[0][0])
                         .scalar())
    
    # * Convert station_last_date to a datetime object
    station_last_date = dt.datetime.strptime(station_last_date, '%Y-%m-%d').date()

    # * Calculate one year prior
    year_prior = station_last_date - dt.timedelta(days=365)
    
    # * Perform left join for the measurment and station tables
    query_2= (session.query(measurement, station.name)
               .outerjoin(station, measurement.station == station.station)
               .filter(measurement.station == most_active_stations[0][0])
               .filter(measurement.date >= str(year_prior))
               .all())

    # TODO: Close session
    session.close()

    # * Loop over the query_2 results to fatch the results needed to create the jsonified result
    result_list = []
    for row in query_2:
        measurement_data = {
            'date': row[0].date,
            'tobs': row[0].tobs,
            'station': row[0].station,
            'station_name': row[1]  
        }
        result_list.append(measurement_data)

    return jsonify(result_list)


# ? ROUTE SOURCE - <start_date>
#?----------------------------------------------------------------
@app.route('/api/v1.0/<start_date>')
def start_date(start_date):
    try:
        # * Convert the input date string to a datetime object
        start = dt.datetime.strptime(start_date, '%Y-%m-%d').date()

        # TODO: Open session
        session = Session(engine)

        # * Query the results from start date onwards based on a user start date
        results = (session.query(
            func.min(measurement.tobs).label('min'),
            func.avg(measurement.tobs).label('avg'),
            func.max(measurement.tobs).label('max')
        ).filter(measurement.date >= start)
        .group_by(measurement.date)
        .all())

        # TODO: Close session
        session.close()

        result_dict = []

        for row in results:
            dictionary = {
                'min': row.min,
                'avg': row.avg,
                'max': row.max
            }
            result_dict.append(dictionary)

        return jsonify(result_dict)

    except ValueError:
        # If the date format is incorrect, return an error message
        return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD format."}), 400
    

# ? ROUTE SOURCE - <start_date>/<end>
#?----------------------------------------------------------------
@app.route('/api/v1.0/<start_date>/<end>')
def start_end(start_date, end):
    try:
        # * Convert the input date string to a datetime object
        start = dt.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = dt.datetime.strptime(end, '%Y-%m-%d').date()

        # TODO: Open session
        session = Session(engine)

        # * Query the results based on two parameters: the start and end periods that a user provides. 
        results = (session.query(
            func.min(measurement.tobs).label('min'),
            func.avg(measurement.tobs).label('avg'),
            func.max(measurement.tobs).label('max')
        ).filter(measurement.date >= start, measurement.date <= end_date)
        .group_by(measurement.date)
        .all())

        # TODO: Close session
        session.close()

        # * Creating a dictionary to hold the results before we jsonify them
        result_dict = []
        for row in results:
            dictionary = {
                'min': row.min,
                'avg': row.avg,
                'max': row.max
            }
            result_dict.append(dictionary)

        return jsonify(result_dict)

    except ValueError:
        # If the date format is incorrect, return an error message
        return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD format."}), 400


if __name__ == '__main__':
    app.run(debug=True)
