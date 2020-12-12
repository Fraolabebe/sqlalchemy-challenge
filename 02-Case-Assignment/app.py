#%%
import sqlalchemy
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import json


from flask import Flask


#%%



#################################################
# Database Setup
#################################################



engine = create_engine('sqlite:///hawaii.sqlite')
conn = engine.connect()

#%%
app = Flask(__name__)



#%%

@app.route("/")
def Homepage():
    """List all available api routes."""
    return (
        f"Welcome!Here all the available Routes to Hawaii temp:<br/>"
        f"/api/v1.0/precipitation<br/r>"
        f"/api/v1.0/stations<br/r>"
        f"/api/v1.0/tobs<br/r>"
        f"/api/v1.0/start<br/r>"
    )

#%%
@app.route('/api/v1.0/precipitation')
def prcp():
    conn = engine.connect()
    query = '''
    SELECT 
        date, 
        prcp
    FROM 
        measurement
    WHERE
        date >= (SELECT DATE (max (date), "-1 year") FROM measurement)
    ORDER BY date DESC
'''
    # Save the query results as a Pandas DataFrame and set the index to the date column
    prcp_df = pd.read_sql(query, conn)
    # Convert the date column to date
    prcp_df['date'] = pd.to_datetime(prcp_df['date'])
    # Sort the dataframe by date
    prcp_df.sort_values('date')
    prcp_json = prcp_df.to_json(orient='records')
    conn.close()
    return prcp_json
   
#%%


@app.route("/api/v1.0/stations")
def stations():
    conn = engine.connect()
    query = '''
    SELECT
        s.station AS station_code,
        s.name AS station_name,
        COUNT(*) as station_count
    FROM
        measurement m
        INNER JOIN station s
        ON m.station = s.station
    GROUP BY 
        s.station,
        s.name
    ORDER BY
        station_count DESC
'''

    active_stations_df = pd.read_sql(query, conn)
    active_stations_df
    stations_json = active_stations_df.to_json(orient='records')
    conn.close()
    return stations_json 
#%%


@app.route("/api/v1.0/tobs")
def tobs():
    conn = engine.connect()
    query = '''
    SELECT
        date,
        tobs
    FROM
        measurement
    WHERE
        date >= (SELECT DATE(MAX(date),'-1 year') FROM measurement)
        AND station = 'USC00519281'
    '''
    temprature_df = pd.read_sql(query, conn)
    temprature_df
    
    temprature_df_json = temprature_df.to_json(orient='records')
    conn.close()
    return temprature_df_json 
#%%


        

#%%
if __name__ == '__main__':
    app.run(debug=True)    
#%%
