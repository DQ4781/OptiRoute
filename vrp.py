import streamlit as st
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Find Euclidean Distance between Two Points
def compute_euclidean_distance_matrix(locations):
    num_locations = len(locations)
    distance_matrix = np.zeros((num_locations, num_locations))

    for i in range(num_locations):
        for j in range(num_locations):
            if i != j:
                distance_matrix[i][j] = np.linalg.norm(np.array(locations[i]) - np.array(locations[j]))
            else:
                distance_matrix[i][j] = 0
    
    return distance_matrix

# Create Data Model for VRP
def create_data_model(numVeh, locations):
    data = {}
    data['distance_matrix'] = compute_euclidean_distance_matrix(locations)
    data['num_vehicles'] = numVeh
    data['depot'] = 0
    return data

# Computer VRP Solution Using ORTools
def compute_vrp(data):
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
        return solution, routing
    else:
        return None, None

def extract_routes(solution, routing, data):
    routes = []
    for vehicle_id in range(data['num_vehicles']):
        route = []
        index = routing.Start(vehicle_id)
        while not routing.IsEnd(index):
            route.append(index)
            index = solution.Value(routing.NextVar(index))
        routes.append(route)
    
    return routes

def main():
    st.title('Vehicle Routing Problem Visualizer')

    # Get User Input
    num_vehicles = st.slider('Number of Vehicles', 1, 10, 3)
    num_destinations = st.slider('Number of destinations', 2, 50, 10)
    
    locations = np.random.rand(num_destinations, 2) * 100

    if st.button('Compute Routes'):
        data = create_data_model(num_vehicles, locations.tolist())
        solution, routing = compute_vrp(data)

        if solution:
            routes = extract_routes(solution, routing, data)
            for index, route in enumerate(routes):
                latitudes = [locations[point][0] for point in route]
                longtitudes = [locations[point][1] for point in route]
                st.write(f"Route for Vehicle {index}: {route}")
                st.map(pd.DataFrame({'lat': latitudes, 'lon':longtitudes}))
        else:
            st.warning("No Solution Found")
    
    st.map(pd.DataFrame(locations, columns=['lat', 'lon']))

if __name__ == '__main__':
    main()