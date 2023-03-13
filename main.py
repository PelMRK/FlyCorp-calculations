import os
import pandas as pd
# import numpy as np
from math import sin, cos, acos, radians, degrees

pd.options.display.max_rows = 999

file_path = "C:/Users/Pel_MRK/Desktop/Pel_MRK/FlyCorp calculations/data/cities.csv"


def add_city(country=None, city=None, auto=False):
    cities = pd.read_csv(file_path)
    if not auto:
        country = input("country:")
        city = input("city:")
        if cities["city"].str.contains(city).sum() > 0:
            print("There is already such city")
            show_results(auto=True, new_city=city)
            return
    city = country + '.' + city
    population = input("population:")
    latitude_degs = input("latitude_degs:")
    latitude_mins = input("latitude_mins:")
    longtitude_degs = input("longtitude_degs:")
    longtitude_mins = input("longtitude_mins:")
    routes_before = calculate_country(country=country, auto=True)
    addition = pd.DataFrame([[country, city, population,
                              latitude_degs, latitude_mins,
                              longtitude_degs, longtitude_mins]],
                            columns=['country', 'city', 'population', 'latitude_degs', 'latitude_mins',
                                     'longtitude_degs', 'longtitude_mins'])
    cities = pd.concat([cities, addition])
    cities.to_csv(file_path, index=False)
    show_results(auto=True, new_city=city, country=country)
    routes_after = calculate_country(country=country, auto=True)
    for key in routes_before:
        if routes_before[key] != routes_after[key]:
            print("Change route: {} to {}".format(key, routes_after[key]))


def show_results(auto=False, new_city=None, country=None, one_country=True):
    cities = pd.read_csv(file_path)
    if not auto:
        country = input("country:")
        city = input("city:")
        new_city = country + '.' + city
        if cities["city"].str.contains(new_city).sum() == 0:
            print("There's no such city yet...")
            add_city(country, city, auto=True)
            return

    print("Calculating...")

    if auto or one_country:
        index = cities[(cities["country"] == country) & (cities["city"] != new_city)]['city']
    else:
        index = cities[cities["country"] != country]['city']

    coefficients = pd.DataFrame(index=index, columns=['coefficient'])

    pop1 = cities[cities["city"] == new_city]["population"]
    pop1 = pop1.iloc[0]

    lat1 = cities[cities["city"] == new_city]["latitude_degs"] + \
           cities[cities["city"] == new_city]["latitude_mins"] / 60
    lat1 = radians(lat1.iloc[0])

    long1 = cities[cities["city"] == new_city]["longtitude_degs"] + \
            cities[cities["city"] == new_city]["longtitude_mins"] / 60
    long1 = radians(long1.iloc[0])

    country_cities = cities.loc[cities["city"].isin(index)]
    country_cities = country_cities[country_cities["city"] != new_city]

    pop2 = country_cities["population"]

    lat2 = (country_cities["latitude_degs"] + country_cities["latitude_mins"] / 60).apply(radians)

    long2 = (country_cities["longtitude_degs"] + country_cities["longtitude_mins"] / 60).apply(radians)

    distance = ((sin(lat1) * lat2.apply(sin) + cos(lat1) * lat2.apply(cos) * (long2 - long1).apply(cos)).apply(
        acos)).apply(degrees) * 111.1
    coefficient = pop1 * pop2 / distance / distance
    coefficients['coefficient'] = coefficient.values

    print(coefficients.sort_values(by='coefficient'))
    print("For - {}".format(new_city))


def calculate_country(country=None, auto=False):
    cities = pd.read_csv(file_path)
    if not auto:
        country = input("country:")
    print("Calculating...")

    cities = cities[cities["country"] == country]
    cities = cities.sort_values(by='latitude_degs', ascending=False)
    routes = {}

    for new_city in cities["city"]:
        pop1 = cities[cities["city"] == new_city]["population"]
        pop1 = pop1.iloc[0]

        lat1 = cities[cities["city"] == new_city]["latitude_degs"] + \
               cities[cities["city"] == new_city]["latitude_mins"] / 60
        lat1 = radians(lat1.iloc[0])

        long1 = cities[cities["city"] == new_city]["longtitude_degs"] + \
                cities[cities["city"] == new_city]["longtitude_mins"] / 60
        long1 = radians(long1.iloc[0])

        index = cities[cities["country"] == country]['city']

        country_cities = cities.loc[cities["city"].isin(index)]
        country_cities = country_cities[country_cities["city"] != new_city]

        pop2 = country_cities["population"]

        lat2 = (country_cities["latitude_degs"] + country_cities["latitude_mins"] / 60).apply(radians)

        long2 = (country_cities["longtitude_degs"] + country_cities["longtitude_mins"] / 60).apply(radians)

        distance = ((sin(lat1) * lat2.apply(sin) + cos(lat1) * lat2.apply(cos) * (long2 - long1).apply(cos)).apply(
            acos)).apply(degrees) * 111.1
        coefficient = pop1 * pop2 / distance / distance
        coefficients = pd.DataFrame(index=cities[cities["city"] != new_city]["city"], columns=['coefficient'])
        coefficients['coefficient'] = coefficient.values

        try:
            routes[new_city] = pd.to_numeric(coefficients['coefficient']).idxmax()
        except Exception:
            print("New country two city case")

        if not auto:
            print("{} --> {}".format(new_city, routes[new_city]))
    if auto:
        return routes


if __name__ == "__main__":
    while True:
        command = input("""
inside country search (1), 
all over the world search (2),
calculate whole country (3)
""")
        if command == '1':
            show_results()
        elif command == '2':
            show_results(one_country=False)
        elif command == '3':
            calculate_country()
    os.system("pause")
