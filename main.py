# Team: Amogus - My Dao and Dexter Kennedy
# student ids: MD - 18181740 and DK - 18778856
# emails: mdao@umich.edu and dexken@umich.edu

import io 
import os
import sys
import requests
import json
import sqlite3
import time
import populate_database


def get_request_census(place, state, api_key):
    response = requests.get(f"https://api.census.gov/data/2021/acs/acs1?get=B19013_001E,group(B19013)&for=place:{place}&in=state:{state}&key={api_key}")
    print("requesting from census")
    if response.status_code == 200:
        try:
            print("returning json")
            return response.json()
        except:
            return response.text
    else:
        print('Request failed with status code:', response.status_code)

def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS iqair
             (id INTEGER PRIMARY KEY AUTOINCREMENT, aqius INTEGER, mainus TEXT, placefp INTEGER, statefp INTEGER)''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS cities
            (placefp INTEGER PRIMARY KEY, statefp INTEGER, median_household_income INTEGER)''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS cities
        (statefp INTEGER PRIMARY KEY, median_household_income INTEGER)''')
    
    conn.commit()

    return cur, conn

def main():
    census_api_key = "d8900686c6c3c3849250269493e9dc13ea71aae8"
    iqair_api_key = "ec767691-84eb-4021-811e-9753abae9c2c"
    #new york
    # census_data = get_request_census("51000", "36", census_api_key)
    # print(census_data)
    # print("median_household_income: {}".format(census_data[1][0]))


    d = requests.get(f"https://api.census.gov/data/2021/acs/acs5/geography&key={census_api_key}")
    print(d.json)

    # Find correct syntax for state and city names
    # states = get_request_iqair('http://api.airvisual.com/v2/states?country=USA&key=', iqair_api_key)
    # print(states)
    # cities_in_dc = get_request_iqair('http://api.airvisual.com/v2/cities?state=Washington, D.C.&country=USA&key=', iqair_api_key)
    # print(cities_in_dc)

    cur, conn = set_up_database("Economics_and_Pollution")

    populate_database.populate_iqair_database(cur, conn, iqair_api_key)


    
if __name__ == '__main__':
    main()