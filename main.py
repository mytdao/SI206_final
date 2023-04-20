# Team: My Dao and Dexter Kennedy
# student ids: MD - 18181740 || DK - 18778856
# emails: mdao@umich.edu || dexken@umich.edu

import io 
import os
import sys
import requests
import json
import sqlite3
import time
import populate_database


def set_up_database(db_name):
    """
    set up 1 data base with 3 tables 
    1 table with air quality index and primary pollutant data from the IQAIR API 
    2 tables with median household income data from the US Census ACS API 
    census tables share a state FIPS integer key 

    Parameters
    ----------
    db_name (str): name given to database 

    Returns
    -------
    cur: cursor execute SQL commands
    conn: connection to the created database
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    # cur.execute(f"DROP TABLE IF EXISTS iqair")
    # cur.execute(f"DROP TABLE IF EXISTS cities")
    # cur.execute(f"DROP TABLE IF EXISTS states")

    cur.execute('''CREATE TABLE IF NOT EXISTS iqair
            (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, state TEXT, aqius INTEGER, mainus TEXT, placefp INTEGER, statefp INTEGER)''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS cities 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, placefp INTEGER, statefp INTEGER, median_household_income INTEGER)''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS states
        (statefp INTEGER PRIMARY KEY, name TEXT, median_household_income INTEGER)''')
    
    conn.commit()

    return cur, conn

def main():
    """
    store Census and IQAIR api keys
    set up a database and populate tables with written functions

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    census_api_key = "d8900686c6c3c3849250269493e9dc13ea71aae8"
    iqair_api_key = "9cab2eb5-7dd7-48d1-8149-8535841f09b4"

    #Find correct syntax for state and city names
    # states = populate_database.get_request_iqair('http://api.airvisual.com/v2/states?country=USA&key=', iqair_api_key)
    # print(states)
    # cities_in_state = populate_database.get_request_iqair('http://api.airvisual.com/v2/cities?state=New York&country=USA&key=', iqair_api_key)
    # print(cities_in_state)

    cur, conn = set_up_database("Economics_and_Pollution")

    populate_database.populate_iqair_and_cities_database(cur, conn, iqair_api_key, census_api_key)
    populate_database.populate_states_database(cur, conn, census_api_key)


    
if __name__ == '__main__':
    main()