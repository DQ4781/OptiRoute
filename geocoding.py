import time
import openrouteservice
import streamlit as st

ors_key = st.secrets["key"]
client = openrouteservice.Client(key=ors_key)


def get_available_cities():
    # Example: Return a hardcoded list of cities
    return [
        "New York, NY",
        "Los Angeles, CA",
        "Chicago, IL",
        "Houston, TX",
        "Phoenix, AZ",
        "Philadelphia, PA",
        "San Antonio, TX",
        "San Diego, CA",
        "Dallas, TX",
        "San Jose, CA",
        "Austin, TX",
        "Jacksonville, FL",
        "Fort Worth, TX",
        "Columbus, OH",
        "Charlotte, NC",
        "San Francisco, CA",
        "Indianapolis, IN",
        "Seattle, WA",
        "Denver, CO",
        "Washington, DC",
        "Boston, MA",
        "El Paso, TX",
        "Nashville, TN",
        "Detroit, MI",
        "Oklahoma City, OK",
        "Portland, OR",
        "Las Vegas, NV",
        "Memphis, TN",
        "Louisville, KY",
        "Baltimore, MD",
        "Milwaukee, WI",
        "Albuquerque, NM",
        "Tucson, AZ",
        "Fresno, CA",
        "Sacramento, CA",
        "Mesa, AZ",
        "Atlanta, GA",
        "Kansas City, MO",
        "Colorado Springs, CO",
        "Omaha, NE",
        "Raleigh, NC",
        "Miami, FL",
        "Long Beach, CA",
        "Virginia Beach, VA",
        "Oakland, CA",
        "Minneapolis, MN",
        "Tampa, FL",
        "Tulsa, OK",
        "Arlington, TX",
        "New Orleans, LA",
    ]


def get_coordinates(cities):
    """
    Convert a list of city names to their corresponding geographic coordinates using ORS.

    :param cities: List of city names.
    :return: List of coordinates (latitude, longitude).
    """
    coordinates = []

    for city in cities:
        try:
            response = client.pelias_search(text=city)
            if response and response["features"]:
                location = response["features"][0]["geometry"]["coordinates"]
                coordinates.append((location[1], location[0]))  # lat, lon
            else:
                print(f"Location not found for city: {city}")
        except Exception as e:
            print(f"Error occurred during geocoding with ORS: {e}")

        time.sleep(1)  # Respect the API rate limit

    return coordinates


def get_single_coordinate(city):
    return get_coordinates([city])[0]
