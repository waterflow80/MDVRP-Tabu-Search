from functools import reduce
from typing import List
from data_structures import *
from utils import *
import re
import math

class TabuListQueue:
    living_iterations_count = 0  # count the number of iterations a change has been saved in the tabu list

    def __init__(self, tabu_list: List[Change] = [], max_living_change=math.inf):
        self.tabu_list = tabu_list
        self.max_living_change = max_living_change  # the number of iterations a change can live in the tabu list before being removed

    def enqueue_change(self, change):
        self.tabu_list.append(change)
        TabuListQueue.living_iterations_count += 1
        if TabuListQueue.living_iterations_count > self.max_living_change:
            self.dequeue_change()


    def dequeue_change(self):
        self.tabu_list.pop(0)


def parse_vehicles_capacity_per_depot(data_file_path:str, problem_data:ProblemData, num_depots:int, num_vehicles:int):
    """Init the vehicles with their corresponding capacity per depot
    Suppose that 'm' represents the number of vehicles per depot"""
    data_file = open(data_file_path, "r")
    lines = data_file.readlines()[1:num_depots+1]
    depots = []
    for i in range(num_depots):
        vehicles = []
        for j in range(num_vehicles):
            vehicle = Vehicle(generate_id(), int(lines[i].split(" ")[1]), i)
            vehicles.append(vehicle)
        depot1 = Depot(i, generate_random_location(), vehicles, [])
        depots.append(depot1)
    problem_data.depots = depots
    data_file.close()


def parse_customers(data_file_path:str, problem_data:ProblemData, num_customers:int, num_depots:int):
    """Loads the customers data and update the given problem_data object
    This function also updates the packages' list of the problem_data object"""
    data_file = open(data_file_path, "r")
    lines = data_file.readlines()[num_depots+1:num_depots+1+num_customers] # Read lines which contains the customers' information
    customers = []
    for line in lines:
        line_elements = re.sub(' +', ' ', line).strip().split(" ") # keep only one space between words, remove extreme spaces, and then splits into a list
        package = Package(generate_id(), int(line_elements[4])) # package
        customer = Customer(int(line_elements[0]), (int(line_elements[1]), int(line_elements[2])), package.id)
        customers.append(customer)
        problem_data.add_package_to_all_depots(package)
    problem_data.customers = customers
    data_file.close()
    return customers

def parse_customers_v2(data_file_path:str):
    """Loads the customers data and update the given problem_data object"""
    data_file = open(data_file_path, "r")
    line = str(data_file.readline()).split(" ")  # The list of the first line's input
    num_customers = int(line[2])
    lines = data_file.readlines()[5:num_customers] # Read lines which contains the customers' information
    customers = []
    for line in lines:
        line_elements: list[str] = re.sub(' +', ' ', line).strip().split(" ") # keep only one space between words, remove extreme spaces, and then splits into a list
        package = Package(generate_id(), int(line_elements[4])) # package
        customer = Customer(int(line_elements[0]), (int(line_elements[1]), int(line_elements[2])), package.id)
        customers.append(customer)
    data_file.close()
    return customers

def load_data(data_file_path:str)->ProblemData:
    """Loads the data from the give data file (.txt file)
    For more information about how to parse the file, please refer to the Instances_description.txt file
    NOTE!: Suppose that 'm' represents the number of vehicles per depot"""
    problem_data = ProblemData()

    data_file = open(data_file_path, "r")
    line = str(data_file.readline()).split(" ") # The list of the first line's input
    num_vehicles = int(line[1])
    num_customers = int(line[2])
    num_depots = int(line[3])
    data_file.close()

    parse_vehicles_capacity_per_depot(data_file_path, problem_data, num_depots, num_vehicles)
    parse_customers(data_file_path, problem_data, num_customers, num_depots)

    return problem_data

def get_all_vehicles(problem_data:ProblemData) -> List[Vehicle]:
    """Return the list of all vehicles in the problemData
    NOTE!: Suppose that 'm' represents the number of vehicles per depot"""
    vehicles = []
    for vehicle_lst in list(map(lambda x: x.vehicles, problem_data.depots)):
        for vehicle in vehicle_lst:
            vehicles.append(vehicle)
    return vehicles

def get_all_customers(problem_data:ProblemData) -> List[Customer]:
    return problem_data.customers

def get_depot_by_id(problem_data:ProblemData, data_file_path:str, depot_id:int)->Depot:
    """Return the depot object given its id
    Return None if not found"""
    for depot_2 in problem_data.depots:
        if depot_2.depotId == depot_id:
            return depot_2

def get_package_by_id(problem_data:ProblemData, package_id:int)->Package:
    for depot_2 in problem_data.depots:
        for package in depot_2.packages:
            if package.id == package_id:
                return package

if __name__ == "__main__":
    load_data("data/p02")