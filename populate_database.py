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


def populate_iqair_and_cities_database(cur, conn, iqair_api_key, census_api_key):
    """
    Store a list of dictionaries with the name, state, place FIPS, and state FIPS
    of 100 popular and diverse US cities. The dictionary values will be used to 
    handle requests to the IQAIR and US Census APIs. A range for loop in conjunction 
    with getting the number of data already in the iqair table will be used to input 
    only 25 elements into each table. 

    Parameters
    ----------
    cur: cursor execute SQL commands
    conn: connection to the created database
    iqair_api_key (str): valid api key to make requests to IQAIR API
    census_api_key (str): valid api key to make requests to US Census API

    Returns
    -------
    None
    """
    cities = [
        {'city': 'New York City', 'state': 'New York', "placefp": "51000", "statefp": "36"},
        {'city': 'Los Angeles', 'state': 'California', "placefp": "44000", "statefp": "06"},
        {'city': 'Chicago', 'state': 'Illinois', "placefp": "14000", "statefp": "17"},
        {'city': 'Houston', 'state': 'Texas', "placefp": "35000", "statefp": "48"},
        {'city': 'Philadelphia', 'state': 'Pennsylvania', "placefp": "60000", "statefp": "42"},
        {'city': 'Phoenix', 'state': 'Arizona', "placefp": "55000", "statefp": "04"},
        {'city': 'San Antonio', 'state': 'Texas', "placefp": "65000", "statefp": "48"},
        {'city': 'San Diego', 'state': 'California', "placefp": "66000", "statefp": "06"},
        {'city': 'Dallas', 'state': 'Texas', "placefp": "19000", "statefp": "48"},
        {'city': 'San Jose', 'state': 'California', "placefp": "68000", "statefp": "06"},
        {'city': 'Austin', 'state': 'Texas', "placefp": "05000", "statefp": "48"},
        {'city': 'Jacksonville', 'state': 'Florida', "placefp": "35000", "statefp": "12"},
        {'city': 'Fort Worth', 'state': 'Texas', "placefp": "27000", "statefp": "48"},
        {'city': 'Columbus', 'state': 'Ohio', "placefp": "18000", "statefp": "39"},
        {'city': 'San Francisco', 'state': 'California', "placefp": "67000", "statefp": "06"},
        {'city': 'Charlotte', 'state': 'North Carolina', "placefp": "12000", "statefp": "37"},
        {'city': 'Indianapolis', 'state': 'Indiana', "placefp": "36003", "statefp": "18"},
        {'city': 'Seattle', 'state': 'Washington', "placefp": "63000", "statefp": "53"},
        {'city': 'Denver', 'state': 'Colorado', "placefp": "20000", "statefp": "08"},
        {'city': 'Washington', 'state': 'Washington, D.C.', "placefp": "50000", "statefp": "11"},
        {'city': 'Boston', 'state': 'Massachusetts', "placefp": "07000", "statefp": "25"},
        {'city': 'Nashville', 'state': 'Tennessee', "placefp": "52006", "statefp": "47"},
        {'city': 'El Paso', 'state': 'Texas', "placefp": "24000", "statefp": "48"},
        {'city': 'Detroit', 'state': 'Michigan', "placefp": "22000", "statefp": "26"},
        {'city': 'Memphis', 'state': 'Tennessee', "placefp": "48000", "statefp": "47"},
        {'city': 'Portland', 'state': 'Oregon', "placefp": "59000", "statefp": "41"},
        {'city': 'Oklahoma City', 'state': 'Oklahoma', "placefp": "55000", "statefp": "40"},
        {'city': 'Las Vegas', 'state': 'Nevada', "placefp": "40000", "statefp": "32"},
        {'city': 'Louisville', 'state': 'Kentucky', "placefp": "48006", "statefp": "21"},
        {'city': 'Baltimore', 'state': 'Maryland', "placefp": "04000", "statefp": "24"},
        {'city': 'Milwaukee', 'state': 'Wisconsin', "placefp": "53000", "statefp": "55"},
        {'city': 'Albuquerque', 'state': 'New Mexico', "placefp": "02000", "statefp": "35"},
        {'city': 'Tucson', 'state': 'Arizona', "placefp": "77000", "statefp": "04"},
        {'city': 'Fresno', 'state': 'California', "placefp": "27000", "statefp": "06"},
        {'city': 'Mesa', 'state': 'Arizona', "placefp": "46000", "statefp": "04"},
        {'city': 'Sacramento', 'state': 'California', "placefp": "64000", "statefp": "06"},
        {'city': 'Atlanta', 'state': 'Georgia', "placefp": "04000", "statefp": "13"},
        {'city': 'Kansas City', 'state': 'Missouri', "placefp": "38000", "statefp": "29"},
        {'city': 'Colorado Springs', 'state': 'Colorado', "placefp": "16000", "statefp": "08"},
        {'city': 'Miami', 'state': 'Florida', "placefp": "45000", "statefp": "12"},
        {'city': 'Raleigh', 'state': 'North Carolina', "placefp": "55000", "statefp": "37"},
        {'city': 'Omaha', 'state': 'Nebraska', "placefp": "37000", "statefp": "31"},
        {'city': 'Long Beach', 'state': 'California', "placefp": "43000", "statefp": "06"},
        {'city': 'Virginia Beach', 'state': 'Virginia', "placefp": "82000", "statefp": "51"},
        {'city': 'Oakland', 'state': 'California', "placefp": "53000", "statefp": "06"},
        {'city': 'Minneapolis', 'state': 'Minnesota', "placefp": "43000", "statefp": "27"},
        {'city': 'Tulsa', 'state': 'Oklahoma', "placefp": "75000", "statefp": "40"},
        {'city': 'Wichita', 'state': 'Kansas', "placefp": "79000", "statefp": "20"},
        {'city': 'Tampa', 'state': 'Florida', "placefp": "71000", "statefp": "12"},
        {'city': 'Aurora', 'state': 'Colorado', "placefp": "04000", "statefp": "08"},
        {'city': 'Santa Ana', 'state': 'California', "placefp": "69000", "statefp": "06"},
        {'city': 'Anaheim', 'state': 'California', "placefp": "02000", "statefp": "06"},
        {"city": "Corpus Christi", "state": "Texas", "placefp": "17000", "statefp": "48"},
        {"city": "Riverside", "state": "California", "placefp": "62000", "statefp": "06"},
        {"city": "Lexington", "state": "Kentucky", "placefp": "46027", "statefp": "21"},
        {"city": "Pittsburgh", "state": "Pennsylvania", "placefp": "61000", "statefp": "42"},
        {"city": "Anchorage", "state": "Alaska", "placefp": "03000", "statefp": "02"},
        {"city": "Stockton", "state": "California", "placefp": "75000", "statefp": "06"},
        {"city": "Cincinnati", "state": "Ohio", "placefp": "15000", "statefp": "39"},
        {"city": "St. Louis", "state": "Missouri", "placefp": "65000", "statefp": "29"},
        {"city": "Toledo", "state": "Ohio", "placefp": "77000", "statefp": "39"},
        {"city": "Newark", "state": "New Jersey", "placefp": "51000", "statefp": "34"},
        {"city": "Greensboro", "state": "North Carolina", "placefp": "28000", "statefp": "37"},
        {"city": "Columbia", "state": "South Carolina", "placefp": "16000", "statefp": "45"},
        {"city": "Henderson", "state": "Nevada", "placefp": "31900", "statefp": "32"},
        {"city": "Lincoln", "state": "Nebraska", "placefp": "28000", "statefp": "31"},
        {"city": "Buffalo", "state": "New York", "placefp": "11000", "statefp": "36"},
        {"city": "Fort Wayne", "state": "Indiana", "placefp": "25000", "statefp": "18"},
        {"city": "Jersey City", "state": "New Jersey", "placefp": "36000", "statefp": "34"},
        {"city": "Saint Paul", "state": "Minnesota", "placefp": "58000", "statefp": "27"},
        {"city": "New Orleans", "state": "Louisiana", "placefp": "55000", "statefp": "22"},
        {"city": "Madison", "state": "Wisconsin", "placefp": "48000", "statefp": "55"},
        {"city": "Lubbock", "state": "Texas", "placefp": "45000", "statefp": "48"},
        {"city": "Chandler", "state": "Arizona", "placefp": "12000", "statefp": "04"},
        {"city": "Scottsdale", "state": "Arizona", "placefp": "65000", "statefp": "04"},
        {"city": "Reno", "state": "Nevada", "placefp": "60600", "statefp": "32"},
        {"city": "Laredo", "state": "Texas", "placefp": "41464", "statefp": "48"},
        {"city": "Winston-Salem", "state": "North Carolina", "placefp": "75000", "statefp": "37"},
        {"city": "Ann Arbor", "state": "Michigan", "placefp": "03000", "statefp": "26"},
        {"city": "Frisco", "state": "Texas", "placefp": "27684", "statefp": "48"},
        {"city": "Boise", "state": "Idaho", "placefp": "08830", "statefp": "16"},
        {"city": "Garland", "state": "Texas", "placefp": "29000", "statefp": "48"},
        {"city": "Hialeah", "state": "Florida", "placefp": "30000", "statefp": "12"},
        {"city": "Alexandria", "state": "Virginia", "placefp": "01000", "statefp": "51"},
        {"city": "Norfolk", "state": "Virginia", "placefp": "57000", "statefp": "51"},
        {"city": "Fremont", "state": "California", "placefp": "26000", "statefp": "06"},
        {"city": "Irvine", "state": "California", "placefp": "36770", "statefp": "06"},
        {"city": "Birmingham", "state": "Alabama", "placefp": "07000", "statefp": "01"},
        {"city": "Rochester", "state": "New York", "placefp": "63000", "statefp": "36"},
        {"city": "San Bernardino", "state": "California", "placefp": "65000", "statefp": "06"},
        {"city": "Spokane", "state": "Washington", "placefp": "67000", "statefp": "53"},
        {"city": "Modesto", "state": "California", "placefp": "48354", "statefp": "06"},
        {"city": "Everett", "state": "Washington", "placefp": "22640", "statefp": "53"},
        {"city": "Tacoma", "state": "Washington", "placefp": "70000", "statefp": "53"},
        {"city": "Shreveport", "state": "Louisiana", "placefp": "70000", "statefp": "22"},
        {"city": "Des Moines", "state": "Iowa", "placefp": "21000", "statefp": "19"},
        {"city": "Grand Rapids", "state": "Michigan", "placefp": "34000", "statefp": "26"},
        {"city": "Augusta", "state": "Georgia", "placefp": "04204", "statefp": "13"},
        {"city": "Mobile", "state": "Alabama", "placefp": "50000", "statefp": "01"},
        {"city": "Albany", "state": "New York", "placefp": "01000", "statefp": "36"}
        ]
    


    cur.execute("SELECT COUNT(*) FROM iqair;")
    i = cur.fetchone()[0]

    for j in range(i, i+25):
        if j < 100:
            city_data = get_request_iqair('http://api.airvisual.com/v2/city?city='+ cities[j]['city'] +'&state='+ cities[j]['state'] +'&country=USA&key=', iqair_api_key)
            print(city_data)
            city_data = city_data['data']['current']['pollution']
            
            
            table_data = (cities[j]['city'], cities[j]['state'], city_data['aqius'], city_data['mainus'], int(cities[j]['placefp']), int(cities[j]['statefp']))
            cur.execute("INSERT INTO iqair (name, state, aqius, mainus, placefp, statefp) VALUES (?, ?, ?, ?, ?, ?)", table_data)
            time.sleep(12)


            mhi_city_data = get_request_MHI_city_census(cities[j]['placefp'], cities[j]['statefp'], census_api_key)
            mhi_city_data = mhi_city_data[1][0]
            
            mhi_table_data = (cities[j]['city'], int(cities[j]['placefp']), int(cities[j]['statefp']), int(mhi_city_data))
            cur.execute("INSERT INTO cities (name, placefp, statefp, median_household_income) VALUES ( ?, ?, ?, ?)", mhi_table_data)

        # "aqius": the air quality index (AQI) calculated based on the US EPA standard, which is an index that indicates how polluted the air is and how hazardous it is to health.
        # "mainus": the primary pollutant that is contributing to the AQI in the US.
    conn.commit()

def populate_states_database(cur, conn, census_api_key):
    """
    Store a list of dictionaries with the name and state FIPS code of 50 US states.
    The dictionary values will be used to handle requests to the US Census API. 
    A range for loop in conjunction with getting the number of data already in the 
    states table will be used to input only 25 elements into the states table. 

    Parameters
    ----------
    cur: cursor execute SQL commands
    conn: connection to the created database
    census_api_key (str): valid api key to make requests to US Census API

    Returns
    -------
    None
    """
    states = [
        {"Alabama": "01"},
        {"Alaska": "02"},
        {"Arizona": "04"},
        {"Arkansas": "05"},
        {"California": "06"},
        {"Colorado": "08"},
        {"Connecticut": "09"},
        {"Delaware": "10"},
        {"District of Columbia": "11"},
        {"Florida": "12"},
        {"Georgia": "13"},
        {"Hawaii": "15"},
        {"Idaho": "16"},
        {"Illinois": "17"},
        {"Indiana": "18"},
        {"Iowa": "19"},
        {"Kansas": "20"},
        {"Kentucky": "21"},
        {"Louisiana": "22"},
        {"Maine": "23"},
        {"Maryland": "24"},
        {"Massachusetts": "25"},
        {"Michigan": "26"},
        {"Minnesota": "27"},
        {"Mississippi": "28"},
        {"Missouri": "29"},
        {"Montana": "30"},
        {"Nebraska": "31"},
        {"Nevada": "32"},
        {"New Hampshire": "33"},
        {"New Jersey": "34"},
        {"New Mexico": "35"},
        {"New York": "36"},
        {"North Carolina": "37"},
        {"North Dakota": "38"},
        {"Ohio": "39"},
        {"Oklahoma": "40"},
        {"Oregon": "41"},
        {"Pennsylvania": "42"},
        {"Rhode Island": "44"},
        {"South Carolina": "45"},
        {"South Dakota": "46"},
        {"Tennessee": "47"},
        {"Texas": "48"},
        {"Utah": "49"},
        {"Vermont": "50"},
        {"Virginia": "51"},
        {"Washington": "53"},
        {"West Virginia": "54"},
        {"Wisconsin": "55"},
        {"Wyoming": "56"}
    ]

    cur.execute("SELECT COUNT(*) FROM states;")
    i = cur.fetchone()[0]

    for j in range(i, i+25):
        if j < 50:
            mhi_state_data = get_request_MHI_state_census(list(states[j].values())[0], census_api_key)
            mhi_state_data = mhi_state_data[1][0]
            
            mhi_table_data = (list(states[j].keys())[0], int(list(states[j].values())[0]), int(mhi_state_data))
            cur.execute("INSERT INTO states (name, statefp, median_household_income) VALUES ( ?, ?, ?)", mhi_table_data)
            
    conn.commit()


def get_request_iqair(url, api_key):
    """
    handle request to IQAIR API and provide error message if unsuccessful 

    Parameters
    ----------
    url (str): valid, correctly formatted url to make requests to IQAIR API
    iqair_api_key (str): valid api key to make requests to IQAIR API

    Returns
    -------
    return a json object if the request was successful 
    return None and print an error message if request was unsuccessful 
    """
    response = requests.get(url + api_key)
    if not response.status_code == 200:
        print('Request failed with status code:', response.status_code)
    return response.json()


def get_request_MHI_city_census(place, state, api_key):
    """
    Handle request to US Census ACS API with provided place (city FIPS code) and
    state (state FIPS code). The function will provide error message if unsuccessful.

    Parameters
    ----------
    place (str): valid city FIPS code
    state (str): valid state FIPS code for the city 
    census_api_key (str): valid api key to make requests to US Census API

    Returns
    -------
    return a json object if the request was successful 
    return None and print an error message if request was unsuccessful 
    """
    response = requests.get(f"https://api.census.gov/data/2021/acs/acs1?get=B19013_001E,group(B19013)&for=place:{place}&in=state:{state}&key={api_key}")
    try:
        return response.json()
    except:
        print('Request failed with status code:', response.status_code)


def get_request_MHI_state_census(state, api_key):
    """
    Handle request to US Census ACS API with provided state (state FIPS code). 
    The function will provide error message if unsuccessful.

    Parameters
    ----------
    state (str): valid state FIPS code for the city 
    census_api_key (str): valid api key to make requests to US Census API

    Returns
    -------
    return a json object if the request was successful 
    return None and print an error message if request was unsuccessful 
    """
    response = requests.get(f"https://api.census.gov/data/2021/acs/acs1?get=B19013_001E,group(B19013)&for=state:{state}&key={api_key}")
    try:
        return response.json()
    except:
        print('Request failed with status code:', response.status_code)