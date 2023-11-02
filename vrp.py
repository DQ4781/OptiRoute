import streamlit as st
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import time
import folium
from folium.plugins import MarkerCluster
import streamlit_folium as st_folium
from dotenv import load_dotenv
import os
import openrouteservice

# Load Env Variables
load_dotenv()

# GLOBAL
GEOLOCATOR = Nominatim(user_agent="myVRPapp")
major_us_cities = [
    "New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX", "Phoenix, AZ", 
    "Philadelphia, PA", "San Antonio, TX", "San Diego, CA", "Dallas, TX", "San Jose, CA",
    "Austin, TX", "Jacksonville, FL", "Fort Worth, TX", "Columbus, OH", "Charlotte, NC",
    "San Francisco, CA", "Indianapolis, IN", "Seattle, WA", "Denver, CO", "Washington, DC",
    "Boston, MA", "El Paso, TX", "Nashville, TN", "Detroit, MI", "Oklahoma City, OK",
    "Portland, OR", "Las Vegas, NV", "Memphis, TN", "Louisville, KY", "Baltimore, MD",
    "Milwaukee, WI", "Albuquerque, NM", "Tucson, AZ", "Fresno, CA", "Sacramento, CA",
    "Mesa, AZ", "Atlanta, GA", "Kansas City, MO", "Colorado Springs, CO", "Omaha, NE",
    "Raleigh, NC", "Miami, FL", "Long Beach, CA", "Virginia Beach, VA", "Oakland, CA",
    "Minneapolis, MN", "Tampa, FL", "Tulsa, OK", "Arlington, TX", "New Orleans, LA"
]

# ENV VARIABLES
ors_key = os.getenv('ORS_KEY')
client = openrouteservice.Client(key=ors_key)

# Create Data Model for VRP
def create_data_model(num_vehicles, locations):
    distance_matrix = client.distance_matrix(
        locations=locations,
        profile='driving-car',
        metrics=["distance"],
        units='mi',
    )['distances']
    
    data = {
        "distance_matrix": distance_matrix,
        "num_vehicles": num_vehicles,
        "depot": 0
    }

    return data

# Computer VRP Solution Using ORTools
def compute_vrp(data):
    """
    Solves the Vehicle Routing Problem using ORTools.
    
    Args:
        data (dict): Data model containing distance matrix, number of vehicles, and depot index.
        
    Returns:
        tuple: A tuple containing the solution, routing model, and index manager.
               Returns None if no solution is found.
    """
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        return data['distance_matrix'][from_index][to_index]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.time_limit.FromSeconds(30)
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        return solution, routing, manager
    else:
        return None, None

def extract_routes(solution, routing, manager):
    """
    Extracts routes from the Vehicle Routing Problem solution.
    
    Args:
        solution: ORTools solution object.
        routing: ORTools routing model object.
        manager: ORTools index manager object.
        
    Returns:
        list: List of routes, each represented as a list of city indices.
    """
    routes = []
    for vehicle_id in range(routing.vehicles()):
        route_for_vehicle = []
        index = routing.Start(vehicle_id)
        while not routing.IsEnd(index):
            point_index = manager.IndexToNode(index)
            route_for_vehicle.append(point_index)
            index = solution.Value(routing.NextVar(index))
        routes.append(route_for_vehicle)
    return routes

def get_lat_lon(city):
    """
    Geocodes a city name to latitude and longitude coordinates using Geopy.
    Delays for 1 second to avoid rate-limiting issues with the geocoding service.
    
    Args:
        city (str): Name of the city.
        
    Returns:
        tuple: A tuple containing latitude and longitude coordinates.
               Returns (None, None) if city coordinates cannot be found.
    """
    location = GEOLOCATOR.geocode(city)
    time.sleep(1)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def plot_routes_on_map(routes, locations):
    """
    Plots extracted routes on a Folium map.
    
    Args:
        routes (list): List of routes, each represented as a list of city indices.
        locations (list): List of tuples containing (latitude, longitude) of cities.
        
    Returns:
        folium.Map: Folium map object displaying routes.
    """
    m = folium.Map(location=locations[0], zoom_start=10)
    markerCluster = MarkerCluster().add_to(m)

    for route in routes:
        full_route_geometry = []

        for point in route:
            location = locations[point]
            folium.Marker(location, icon=folium.Icon(color='blue')).add_to(markerCluster)

        for i in range(len(route)-1):
            start_coord = locations[route[i]]
            end_coord = locations[route[i+1]]

            route_directions = client.directions(
                coordinates=[start_coord, end_coord],
                profile='driving-car',
                format='geojson'
            )

            route_geometry = route.directions['features'][0]['geometry']['coordinates']
            full_route_geometry += route_geometry
        
        folium.PolyLine(full_route_geometry, color='blue', weight=2.5, opacity=1).add_to(m)
    
    return m

def main():
    st.title('Vehicle Routing Problem Visualizer')

    # Get User Input
    num_vehicles = st.slider('Number of Vehicles', 1, 10, 3)
    cities = st.multiselect('Choose cities:', major_us_cities)

    locations = [get_lat_lon(city) for city in cities]

    if st.button('Compute Routes'):
        data = create_data_model(num_vehicles, locations)
        solution, routing, manager = compute_vrp(data)

        if solution:
            routes = extract_routes(solution, routing, manager)

            map_with_all_routes = plot_routes_on_map(routes, locations)

            st_folium.folium_static(map_with_all_routes)
        else:
            st.warning("No Solution Found")
    

if __name__ == '__main__':
    main()