# MDVRP-Tabu-Search
This is an implementation of the Tabu Search algorithm to solve a MDVRP (Multi-Depot Vehicle Routing Problem)  problem given probem test instances.

## Tabu Search
Tabu search (TS) is a metaheuristic search method employing local search methods used for mathematical optimization. It was created by Fred W. Glover in 1986 and formalized in 1989. [(Wikipedia)](https://en.wikipedia.org/wiki/Tabu_search)

Local (neighborhood) searches take a potential solution to a problem and check its immediate neighbors (that is, solutions that are similar except for very few minor details) in the hope of finding an improved solution. [(Wikipedia)](https://en.wikipedia.org/wiki/Tabu_search)

Tabu search enhances the performance of local search by relaxing its basic rule. First, at each step worsening moves can be accepted if no improving move is available (like when the search is stuck at a strict local minimum). In addition, prohibitions (hence the term tabu) are introduced to discourage the search from coming back to previously-visited solutions. [(Wikipedia)](https://en.wikipedia.org/wiki/Tabu_search)

## Main Idea
![Screenshot from 2024-03-06 17-05-19](https://github.com/waterflow80/MDVRP-Tabu-Search/assets/82417779/9479391c-630a-42c0-8033-ef7f031166f0)

The main idea behind the MDVRP problem is that we have multiple depots displaced in different locations, each depot contains a number of vehicles,and each vehicle has a certain capacity.

Given a number of customers, each with a package request (with a given size), we should find the best routes that minimizes the overall cost of delivery (in our cast the cost is the overall distance made by all vehicles in the delivery process). 

## Input Data - Problem Definition
The test instance should contain the following data:
- **Depots**: we should know the number of available depots (**Note!:** currently we're assigning a random coordinates for each depot at the start of each execution, we should consider making it constant).
- **Vehicles**: we should know the number of available vehicles in each depot (in our test data the number is the same for all depots).
- **Customers**: we should know the number of customers and for each customer, his **id**, **coordinates (x,y)**, **demand** (the size of the package), and possibly other information.

We can notice that the number of routes in the solution will be the same as the number of vehicles used. **num_routes = num_used_vehicles**

## Data Structures
Here's an insight of some of the most important data structures used in our implementation. All data structures can be found in the [data_structures.py](https://github.com/waterflow80/MDVRP-Tabu-Search/blob/main/data_structures.py) file.
The `ProblemData` object will hold the problem information parsed from the test data files:
```python
class ProblemData:
  def __init__(self, numDepots:int=0, depots:List[Depot]=None, numCustomers:int=0, customers:List[Customer]=None) -> None:
    self.numDepots = numDepots
    self.depots = depots
    self.numCustomers = numCustomers
    self.customers = customers
```
The `Solution` object represents the final solution object that we're looking to find.
```python
class Solution:
  def __init__(self, routes:List[Route]=[], numUsedCars:int=0, cost:float=0.0) -> None:
    self.routes = routes
    self.numUsedCars = numUsedCars
    self.cost = cost
```
The `Route` object contains information about a specific route. It's `route` attribute contains the customers visited in order (their order in the list):
```python
class Route:
  def __init__(self, route_id:int, starting_depot:Depot, customers_ordered:List[Customer], vehicle=None) -> None:
    self.route_id = route_id
    self.startingDepot = starting_depot
    self.route = customers_ordered # [customer1{indx:0}, customer2{indx:1}, ...]
    self.vehicle = vehicle
```

## How to read the code
In order to easily understand the code, we recommend that you start with `main.py`, since it contains the main general algorithm, and then start looking at the `tabu.py` which contains implmentations of most of the functions used in main.py. 

At any time, while reading the algorithm, you can refer to the `data_structures.py` file in order to know what every class or object is made of.

## Run
To run the code locally, you can follow the following steps (Linux, but very similar to Windows):
```bash
git clone https://github.com/waterflow80/MDVRP-Tabu-Search.git
cd MDVRP-Tabu-Search
# Edit your hyper-paramters in main.py (at the top of the script)
python3.x main.py # This will run the algorithm on all the test files under `data/`
```

## Things to note
The data.py was used to parse our initial `data.json` test data file, and it is no longer used. There have been some changes in the data structures, eg: `float --> int` some attributes, etc. So be sure to check them before using `data.py` and the `data.json` test data.

## Current Limitations/Possible Enhancements
- Currently the `generate_random_solution()` function is fully random, and it may sometimes give bad results, unless executed several times to increase the probability of getting different configuration. So we should consider using some heuristics on that function and make it not commpletly random.
- We can consider using multi-threaing and parrallel programming to increase performance.

## Final Words
If you find it useful, we appreciate that you give it a star.
