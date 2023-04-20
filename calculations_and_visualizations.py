import io 
import os
import sys
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

def main():
    """
    Connects to the database and opens a file for writing before calling helper functions that
    make calculations and visualizations using the database data and write to the file.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+"Economics_and_Pollution")
    cur = conn.cursor()

    income_disparity = {}
    pollution_factors = {}
    aqi_scores = {}
    city_aqi_scores = {}

    with open('pollution_and_income_calculations.txt', 'w') as f:

        income_disparity = calculate_disparity(cur, f)
        pollution_factors, aqi_scores, city_aqi_scores = calculate_pollution_factors(cur, f)
    
    visualize_data(income_disparity, pollution_factors, aqi_scores, city_aqi_scores)




def calculate_disparity(cur, f):
    """
    Parameters
    ----------
    cur: The connection cursor
    f: The file handle

    Returns
    -------
    Income_disparity: A list of dictionaries with each dictionary having a key for city_name, state_name, city_median_income, state_median_income, and income_disparity

    Retrieves data from the cities and states table joined on statefp then uses the data to construct the income_disparity
    list of dictionaries while printing out each cities data.
    """
    income_disparity = []

    for state_code in range(57):

        cur.execute("SELECT cities.name, states.name, cities.median_household_income, states.median_household_income FROM cities JOIN states ON cities.statefp = states.statefp AND states.statefp = ?", (state_code, ))
        data = cur.fetchall()

        if len(data) > 0:
            print(data)

            for row in data:
                temp_dict = {"city_name": row[0], "state_name": row[1], "city_median_income": row[2], "state_median_income": row[3], "income_disparity": row[2] - row[3]}
                income_disparity.append(temp_dict)
                f.write(f"The income disparity for the city of {temp_dict['city_name']} is {temp_dict['income_disparity']} when compared to the state average of {temp_dict['state_median_income']}\n")
    
    print(income_disparity)
    return income_disparity




def calculate_pollution_factors(cur, f):
    """
    Parameters
    ----------
    cur: The connection cursor
    f: The file handle

    Returns
    -------
    pollution_factors: A dictionary of the total main pollutants in the cities
    aqi_scores:The sum of all aqi scores for cities with each major pollutant 
    city_aqi_scores: A dictionary of aqi scores for each city

    Reads data from the iqair table and parses through the data to construct the output dictionaries.
    While it constructs the dictionaries it outputs the calculated data to the inputted file handle
    """

    pollution_factors = {}
    aqi_scores = {}
    city_aqi_scores = {}

    cur.execute("SELECT name, aqius, mainus FROM iqair")
    data = cur.fetchall()

    for row in data:
        if row[2] in pollution_factors:
            pollution_factors[row[2]] += 1
            aqi_scores[row[2]] += row[1]
        else:
            pollution_factors[row[2]] = 1
            aqi_scores[row[2]] = row[1]

        city_aqi_scores[row[0]] = row[1]

    # print(pollution_factors)
    # print(aqi_scores)
    # print("\n\n\n")
    # print(city_aqi_scores)

    for key in pollution_factors:
        avg_aq = aqi_scores[key]/pollution_factors[key]
        f.write(f"There are {pollution_factors[key]} cities with {key} as their main pollutant\n")
        f.write(f"The average air quality for cities with {key} as their main pollutant is {avg_aq}\n")

    return pollution_factors, aqi_scores, city_aqi_scores



def visualize_data(income_disparity, pollution_factors, aqi_scores, city_aqi_scores):    
    """
    Parameters
    ----------
    Income_disparity: A list of dictionaries with each dictionary having a key for city_name, state_name, city_median_income, state_median_income, and income_disparity
    pollution_factors: A dictionary of the total main pollutants in the cities
    aqi_scores:The sum of all aqi scores for cities with each major pollutant 
    city_aqi_scores: A dictionary of aqi scores for each city

    Returns
    -------
    None

    Uses the passed in data to create three visualizations.
    One being a barchart of which pollutants are the main polluters or cities.
    The second being the average AQI score for cities with each main pollutant.
    The third being a scatterplot of AQI scores and income disparity.
    """   
    #Number of Cities with Each Major Pollutant
    labels = ["CO", "NO2", "SO2"]
    labels.extend(list(pollution_factors.keys()))
    labels.extend(["p10", "O3"])
    pollution_values = [0, 0, 0]
    pollution_values.extend(list(pollution_factors.values()))
    pollution_values.extend([0, 0])

    print(labels)
    print(pollution_values)
    plt.bar(labels, pollution_values)
    plt.xlabel('Types of Major Pollutants')
    plt.ylabel('Number of Cities')
    plt.title('Number of Cities with Each Major Pollutant')
    plt.savefig("num_city_pollutants.png")
    plt.close()


    #Number of Cities within Air Quality Index Score
    values = list(city_aqi_scores.values())
    bin_edges = np.arange(0, max(values) + 5, 5)
    hist, bins = np.histogram(values, bins=bin_edges)

    colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'navy', 'springgreen', 'pink', 'cyan']
    plt.bar(bins[:-1], hist, width=5, color = colors)
    plt.xlabel("United States Air Quality Index Score")
    plt.ylabel("Number of Cities")
    plt.title('Number of Cities within Air Quality Index Score')
    plt.savefig("barchart_of_aqi.png")
    plt.close()

    #Air Quality Index Values vs. Income Disparity
    x = []
    y = []
    city_labels = []

    for row in income_disparity:
        x.append(row['income_disparity'])
        city_labels.append(row['city_name'])
        y.append(city_aqi_scores[row['city_name']])

    print("\n\n\n")
    print(x)
    print(y)

    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set_ylim(0, 100)

    # for i in range(len(city_labels)):
    #     plt.text(x[i], y[i], city_labels[i])

    ax.set_xlabel('Income Disparity of Cities Compared to State Average')
    ax.set_ylabel('United States Air Quality Index Values')
    ax.set_title('Air Quality Index Values vs. Income Disparity')
    fig.savefig("air_quality_vs_income.png")



if __name__ == '__main__':
    main()