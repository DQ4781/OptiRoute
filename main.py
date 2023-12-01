import streamlit as st
import streamlit_folium as st_folium
import vrp_solver
import geocoding
import route_services
import map_visualization

def run_vrp_solver(num_vehicles, cities, depot):
    try:
        # Convert city names to coordinates
        locations = geocoding.get_coordinates(cities)
        #depot_location = geocoding.get_single_coordinate(depot)

        # Compute Routes
        routes = vrp_solver.solve_vrp(locations, num_vehicles, depot)

        # Visualize Routes
        map_with_routes = map_visualization.plot_routes(routes, locations)
        st_folium.folium_static(map_with_routes)
    except Exception as e:
        st.error(f"An error occured: {e}")

def main():
    st.title("Vehicle Routing Problem Visualizer")

    # User Inputs for VRP
    num_vehicles = st.slider("Number of Vehicles", 1, 10, 3)
    cities = st.multiselect("Choose Cities:", geocoding.get_available_cities())
    depot_city = st.selectbox("Choose Depot City:", cities)
    if depot_city is not None:
        depot_index = cities.index(depot_city)

    if st.button("Compute Routes"):
        run_vrp_solver(num_vehicles, cities, depot_index)


if __name__ == '__main__':
    main()