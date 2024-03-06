from data2 import load_data, get_all_vehicles, get_all_customers, get_depot_by_id, get_package_by_id, TabuListQueue
from data_structures import *
from utils import generate_id
import random
import math

# Variables - Data
#problemData = load_data()
# T = [] # Tabu list (contains the list of changes)

# Functions
def remove_elements_from_list(main_list, to_remove_list)->None:
    """remove the elements of target_customers from all_customers"""
    for elt in to_remove_list:
        main_list.remove(elt)


def get_required_capacity(problem_data:ProblemData, target_customers:List[Customer])->int:
    """Return the required capacity for the packages of the given customers"""
    required_capacity = 0
    for customer in target_customers:

        package = get_package_by_id(problem_data, customer.packgaeId)
        required_capacity += package.size
    return required_capacity

def verify_vehicle_capacity(problem_data:ProblemData, target_customers:List[Customer], vehicle:Vehicle)->bool:
    """verify that the given vehicle can carry out the packages of the given target_customers"""
    vehicle_capacity = vehicle.capacity
    required_capacity = get_required_capacity(problem_data, target_customers)
    #print("VEHICLE CAPACITY: ", vehicle_capacity)
    #print("REQUIRED CAPACITY: ", required_capacity)
    return vehicle_capacity >= required_capacity


def get_possible_customers(problem_data:ProblemData, customers_list:List[Customer], vehicle:Vehicle):
    """Return the list of customers that the given vehicle can serve"""
    vehicle_capacity = vehicle.capacity
    customers_served = 0
    required_capacity = 0
    result_customers = []
    while customers_served < len(customers_list) and required_capacity < vehicle_capacity:
        max_capacity_customer = max(customers_list, key=lambda x: get_package_by_id(problem_data, x.packgaeId).size)
        customers_list.remove(max_capacity_customer)
        if get_required_capacity(problem_data, [max_capacity_customer]) < vehicle.capacity:
            result_customers.append(max_capacity_customer)
            customers_served += 1
            required_capacity += get_package_by_id(problem_data, max_capacity_customer.packgaeId).size
    return result_customers


def generate_random_solution(data_file_path:str)->Solution:
    """generate a random solution out of the problemData"""
    # TODO include the capacity of the vehicles in the calculations
    # TODO just make a formula
    problem_data = load_data(data_file_path)
    all_vehicles = get_all_vehicles(problem_data)
    all_customers = get_all_customers(problem_data)
    random.shuffle(all_customers) # add randomness in the selection of customers
    solution = Solution()
    i = 0
    while i < len(all_vehicles) and len(all_customers) > 0:
        # still customers to serve
        if i != len(all_vehicles) - 1:
            target_customers = random.sample(all_customers, random.randrange(1, len(all_customers)+1))
            while not verify_vehicle_capacity(problem_data, target_customers, all_vehicles[i]):
                # print("Vehicle capacity not respected!")
                #TODO: Can be optimized to reduce the calculation time for this process
                #TODO: Don't take it random, but rather one by one sequentially
                target_customers = random.sample(all_customers, random.randrange(1, len(all_customers)+1))
        else:
            # last vehicle, take all the remaining customers
            target_customers = get_possible_customers(problem_data, all_customers[0:], all_vehicles[i])
        start_depot = get_depot_by_id(problem_data, data_file_path, all_vehicles[i].depotId)
        route = Route(generate_id(),start_depot, target_customers, all_vehicles[i])
        solution.addRoute(route)
        remove_elements_from_list(all_customers, target_customers)  # remove the chosen customers
        i += 1
    solution.cost = evaluate(solution)
    # print("--------------TESTING---------------")
    # print("SOLUTION EVAL=>", evaluate(solution))
    # print("SOLUTION COST=>", solution.cost)
    # print("--------------------------------------")
    return solution


def get_all_sol_customers(current_sol:Solution)->List[SolCustomer]:
    """Return the list of all customers, each in the form of SolCustomer"""
    sol_customers = []
    for route in current_sol.routes:
        for i in range(len(route.route)):
            sol_customer = SolCustomer(route.route[i], route.route_id, i)
            sol_customers.append(sol_customer)
    return sol_customers


def insert_customer_at_solution_route_at_index(current_sol:Solution, customer:Customer, route_id:int, index_in_route:int):
    """Insert the given customer in the given solution at the given index in the route
    Override the existing"""
    # print("ROUTE BEFORE ", end="")
    # for cust in current_sol.routes[0].route:
    #     print(cust.id, end=", ")
    # print()
    for route1 in current_sol.routes:
        if route1.route_id == route_id:
            #print("INSERTING CUSTOMER", customer.id, "IN ROUTE ", route1.route_id, "AT INDEX", index_in_route)
            route1.route[index_in_route] = customer
    # print("CURRENT ROUTE ",end="")
    # for cust in current_sol.routes[0].route:
    #     print(cust.id, end=", ")
    # print()
    return current_sol


def switch_customers_in_solution(current_sol:Solution, sol_customers:List[SolCustomer])->Solution:
    import copy
    """Switch the position of the given two customers in the given solution
    and return the resulting solution"""
    temp_sol1 = copy.deepcopy(current_sol)
    # print("------------------------------")
    # print("SWITCHING CUSTOMER", sol_customers[0].customer.id, "(ROUTE "+ str(sol_customers
    #                                            [0].route_id) + ", Indx: "+ str(sol_customers[0].index_in_route) +") WITH CUSTOMER", sol_customers[1].customer.id, "(ROUTE "+ str(sol_customers
    #                                            [1].route_id) + ", Indx: "+ str(sol_customers[1].index_in_route) + ")")
    temp_sol1 = insert_customer_at_solution_route_at_index(temp_sol1,
                                               sol_customers[0].customer, sol_customers
                                               [1].route_id, sol_customers[1].index_in_route)
    temp_sol1 = insert_customer_at_solution_route_at_index(temp_sol1,
                                               sol_customers[1].customer, sol_customers
                                               [0].route_id, sol_customers[0].index_in_route)
    #print("ORDER" current_sol.routes)
    #print("------------------------------")
    return temp_sol1


def generate_neighbor_solutions(current_sol:Solution, num_neighbors:int, tabu_list:TabuListQueue)->List[SolutionChangePair]:
    """ generate num_neighbors neighbor solutions and save the change of each solution in T
    see docs in the Readme file"""
    sol_change_pairs = []
    sol_customers = get_all_sol_customers(current_sol)  # a list of SolCustomer objects
    for i in range(num_neighbors):
        sol_change_pair = SolutionChangePair()
        sample_sol_customers = random.sample(sol_customers, 2) # the two customers to switch
        new_solution = switch_customers_in_solution(current_sol, sample_sol_customers)
        new_solution.cost = evaluate(new_solution)
        # print("++++++++++CURRENT++++++++++++")
        # for cust in current_sol.routes[0].route:
        #     print(cust)
        # print("+++++++++++++++++++++++++++++")
        # print("++++++++++NEW++++++++++++++++")
        # for cust in new_solution.routes[0].route:
        #     print(cust)
        #print("+++++++++++++++++++++++++++++")

        sol_change_pair.solution = new_solution
        sol_change_pair.change = Change(sample_sol_customers[0].customer, sample_sol_customers[1].customer)
        sol_change_pairs.append(sol_change_pair)
        tabu_list.enqueue_change(sol_change_pair.change)
    return sol_change_pairs

def allowed(sol_change_pairs: List[SolutionChangePair], tabu_list:TabuListQueue, tabu_tenure:int)->List[Solution]:
    """return only the allowed solutions from the given solution
    in which the change """
    allowed_solutions = []
    for solChangePair in sol_change_pairs:
        if solChangePair.change in tabu_list.tabu_list and tabu_list.tabu_list.count(solChangePair.change) > tabu_tenure:
            continue
        # else: allowed
        allowed_solutions.append(solChangePair.solution)
    return allowed_solutions


def best(sols:List[Solution])->Solution:
    """Return the best solution from the given solutions
    based on their eval() result (the lesser the best)"""
    assert len(sols) > 0
    return min(sols, key=lambda sol: evaluate(sol))

def best_from_sol_change_pairs(sol_change_pairs: List[SolutionChangePair])->Solution:
    """Return the best solution from the given solutions"""
    sols = list(map(lambda scp: scp.solution, sol_change_pairs))
    return best(sols)



def calculate_distance_two_nodes(node1:Node, node2:Node)->float:
    """Return the Euclidean distance between the given two nodes
       Note: the given node should have a 'location' attribute"""
    return math.sqrt(math.pow(node1.location[0] - node2.location[0], 2) + math.pow(node1.location[1] - node2.location[1], 2))


def calculate_route_distance(route:Route)->float:
    distance = 0.0
    # 1. distance from staring depot to the first customer
    distance +=  calculate_distance_two_nodes(route.startingDepot, route.route[0])
    # 2. distance from the customers (ordered)
    for i in range(len(route.route)-1):
        distance += calculate_distance_two_nodes(route.route[i], route.route[i + 1])
    # 3. distance from the last customer to the starting depot
    distance += calculate_distance_two_nodes(route.route[len(route.route)-1], route.startingDepot)
    return distance


def evaluate(sol:Solution) -> float:
    """return the overall distance of all routes in the given solution"""
    distance = 0.0
    for route in sol.routes:
        distance += calculate_route_distance(route)
    return distance

if __name__ == "__main__":
    solution = generate_random_solution()
    for route in solution.routes:
        print(route)
    print("EVALUATION: ", solution.cost)