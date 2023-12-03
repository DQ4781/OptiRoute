import openrouteservice
import streamlit as st

ors_key = st.secrets["key"]

client = openrouteservice.Client(key=ors_key)


def get_distance_matrix(locations):
    try:
        matrix = client.distance_matrix(
            locations=locations, profile="driving-car", metrics=["distance"], units="mi"
        )
        return matrix["distances"]
    except Exception as e:
        print(f"Error in getting distance matrix: {e}")
        return None


def get_route_directions(start_coord, end_coord):
    try:
        route = client.directions(
            coordinates=[start_coord, end_coord],
            profile="driving-car",
            format="geojson",
        )
        return route
    except Exception as e:
        print(f"Error in getting route directions: {e}")
        return None
