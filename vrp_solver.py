from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def solve_vrp(distance_matrix, num_vehicles, depot):
    """
    Solves the Vehicle Routing Problem.

    :param distance_matrix: Matrix of distances between locations.
    :param num_vehicles: Number of vehicles available.
    :param depot: Index of the depot location.
    :return: A list of routes for each vehicle.
    """
    # Create the routing index manager
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), num_vehicles, depot)

    # Create Routing Model
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback
    def distance_callback(from_index, to_index):
        # Convert from routing variable Index to distance matrix NodeIndex
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Set parameters for search
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem
    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        return extract_routes(solution, routing, manager)
    else:
        return []

def extract_routes(solution, routing, manager):
    """
    Extract routes from the solution.

    :param solution: The VRP solution.
    :param routing: The routing model.
    :param manager: The routing index manager.
    :return: A list of routes for each vehicle.
    """
    routes = []
    for vehicle_id in range(routing.vehicles()):
        route = []
        index = routing.Start(vehicle_id)
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        routes.append(route)
    return routes
