import json
from typing import List
from data_structures import *

DATA_FILE = "data.json" # The data of the problem

def parseVehicles(depot:dict)->List[Vehicle]:
  vehicles = []
  for vehicle in depot["vehicles"]:
    vehicle1 = Vehicle(vehicle["vehicleId"], vehicle["capacity"], depot["depotId"])
    vehicles.append(vehicle1)
  return vehicles

def parsePackages(depot:dict)->List[Package]:
  packages = []
  for package in depot["packages"]:
    package1 = Package(package["packageId"], package["size"])
    packages.append(package1)
  return packages


def parseDepots(data:dict)->List[Depot]:
  depots = []
  for depot in data["depots"]:
    vehicles = parseVehicles(depot)
    packages = parsePackages(depot)
    depot = Depot(depot["depotId"], tuple(depot["location"]), vehicles, packages)
    depots.append(depot)
  return depots

def parseCustomers(data:dict)->[Customer]:
  customers = []
  for customer in data["customers"]:
    customer1 = Customer(int(customer["customerId"]), customer["location"], customer["packageId"])
    customers.append(customer1)
  return customers

def load_data()->ProblemData:
  data_file = open(DATA_FILE)
  data1 = json.load(data_file)

  numDepots = len(data1["depots"])
  numCustomers = len(data1["customers"])
  depots = parseDepots(data1)
  customers = parseCustomers(data1)
  data_file.close()
  
  return ProblemData(numDepots, depots, numCustomers, customers)

def load_dict_data()->dict:
  """load the data and return it in a dict format"""
  data_file = open(DATA_FILE)
  data1 = json.load(data_file)
  data_file.close()
  return data1

def get_num_vehicles(data: ProblemData) -> int:
  """return the number of vehicles given the problem data"""
  num = 0
  for depot in data.depots:
    num += len(depot.vehicles)
  return num

def get_depot_by_id(depot_id:int)->Depot:
  """return the depot object given its id"""
  pb_data = load_dict_data()
  for depot1 in pb_data["depots"]:
    if depot1["depotId"] == depot_id:
      vehicles = parseVehicles(depot1)
      packages = parsePackages(depot1)
      return Depot(depot1["depotId"], depot1["location"], vehicles, packages)

def get_all_vehicles()->List[Vehicle]:
  pb_data = load_dict_data()
  vehicles = []
  for depot in pb_data["depots"]:
    vehicles.extend(parseVehicles(depot))
  return vehicles

def get_all_customers()->List[Customer]:
  pg_data = load_dict_data()
  return parseCustomers(pg_data)

if __name__ == "__main__":
  data = load_data()
  print(data.depots[0].vehicles[0])
