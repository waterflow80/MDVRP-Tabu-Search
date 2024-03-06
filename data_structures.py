from typing import List, Tuple

class Vehicle :
  def __init__(self, vehicle_id:int, capacity:int, depotId:int) -> None:
    # The capacity is the number of packages it can deliver (can be changed later)
    self.id = vehicle_id
    self.capacity = capacity  # number of packages it can load (regardless of size, can be enhanced)
    self.depotId = depotId
  
  def __str__(self) -> str:
    return "Vehicle={id=" + str(self.id) + ", capacity=" + str(self.capacity) +"}"

class Package:
  def __init__(self, package_id:int, size:int) -> None:
    self.id = package_id
    self.size = size # m³ Metre Cube

class Node:
  def __init__(self, location:Tuple[float])->None:
    self.location = location

class Customer(Node):
  def __init__(self, customer_id:int, location:Tuple[int, int], packageId:int) -> None:
    super().__init__(location)
    self.id = customer_id
    self.packgaeId = packageId # the id of the requested package
  
  def __str__(self) -> str:
    return "Customer={id=" + str(self.id) + ", location=" + str(self.location) + ", packageId=" + str(self.packgaeId) +"}"

class Station:
  def __init__(self, customer:Customer, index:int) -> None:
    self.customer = customer
    self.index = index # at what turn it has been reached

class Change:
  def __init__(self, customer1:Customer, customer2:Customer) -> None:
    self.customer1 = customer1
    self.customer2 = customer2

  def __str__(self) -> str:
    return "[customer1={" + str(self.customer1.id) + "}, customer2={" + str(self.customer2.id) + "}]"

class Depot(Node):
  def __init__(self, depot_id:int=0, location:Tuple[int, int]=None, vehicles: List[Vehicle]=[], packages:List[Package]=[]) -> None:
    super().__init__(location)
    self.depotId = depot_id
    self.vehicles = vehicles
    self.packages = packages

  def __str__(self) -> str:
    return "Depot={" + "id=" + str(self.depotId) + ", location="+ str(self.location) + ", vehicles=" + self.vehicles.__str__() + ", packages="+ self.packages.__str__() + "}"

class Route:
  def __init__(self, route_id:int, starting_depot:Depot, customers_ordered:List[Customer], vehicle=None) -> None:
    self.route_id = route_id
    self.startingDepot = starting_depot
    self.route = customers_ordered # [customer1{indx:0}, customer2{indx:1}, ...]
    self.vehicle = vehicle

  def __str__(self) -> str:
    routes_repr = "-------------------------------------------- ROUTE " + str(self.route_id) +" --------------------------------------------\n"
    routes_repr += "depot(" + str(self.startingDepot.depotId) + "): Vehicle("+ str(self.vehicle.id) +")\n"
    for customer in self.route:
      routes_repr += " --> " + customer.__str__() + "\n"
    routes_repr += "------------------------------------------ END ROUTE --------------------------------------------\n"
    return routes_repr

class SolCustomer:
  """This is an intermediate class that will be used to store a customer of a
  solution, along with its coordinates within the solution"""
  def __init__(self, customer:Customer, route_id:int, index_in_route:int)->None:
    self.customer = customer
    self.route_id = route_id
    self.index_in_route = index_in_route

class Solution:
  def __init__(self, routes:List[Route]=[], numUsedCars:int=0, cost:float=0.0) -> None:
    self.routes = routes
    self.numUsedCars = numUsedCars
    self.cost = cost

  def addRoute(self, route:Route) -> None:
    self.routes.append(route)
  def setNumUsedCars(self, numUsedCars:int)->None:
    self.numUsedCars = numUsedCars
  def setCost(self, cost:float)->None:
    self.cost = cost

  def __str__(self) -> str:
    return "Solution = {" + self.routes.__str__() + ", numUsedCars=" + str(self.numUsedCars) + ", cost=" + str(self.cost) +"}"

class SolutionChangePair:
  def __init__(self, solution:Solution=None, change:Change=None) -> None:
    self.solution = solution
    self.change = change

class ProblemData:
  def __init__(self, numDepots:int=0, depots:List[Depot]=None, numCustomers:int=0, customers:List[Customer]=None) -> None:
    self.numDepots = numDepots
    self.depots = depots
    self.numCustomers = numCustomers
    self.customers = customers

  def add_package_to_all_depots(self, package:Package) -> None:
    """adds the given package to all the depots"""
    for depot_1 in self.depots:
      depot_1.packages.append(package)

  def __str__(self) -> str:
    repr = "ProblemData={\nDepots="
    for depot in self.depots:
      repr += depot.__str__()
    repr += "\n"
    for customer in self.customers:
      repr += customer.__str__()
    repr += "}"
    return repr



if __name__ == "__main__":
  depot = Depot(1, (1.5, 54.1), [Vehicle(5, 3.0), Vehicle(6, 1.0)])
  print(depot.depotId)
  print(depot.location)
  print(depot.vehicles[0])

