import folium

def plot_routes(routes, locations):
    """
    Plot the routes on a map.

    :param routes: A list of routes, where each route is a list of location indices.
    :param locations: List of coordinates (latitude, longitude).
    :return: A Folium map object with plotted routes.
    """
    # Assuming the first location is the depot
    map_object = folium.Map(location=locations[0], zoom_start=12)

    # Colors for different routes
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']

    for vehicle_id, route in enumerate(routes):
        color = colors[vehicle_id % len(colors)]
        for i in range(len(route) - 1):
            start_coords = locations[route[i]]
            end_coords = locations[route[i + 1]]
            folium.Marker(start_coords, icon=folium.Icon(color=color)).add_to(map_object)
            folium.PolyLine([start_coords, end_coords], color=color, weight=2.5, opacity=1).add_to(map_object)

    return map_object
