# MDVRP + Tabu Search
Sloving a MDVRP problem using the Tabu Search method

## Definitions
- **Neighbor solution:** a solution in which there's a change in the order of route between two customers

## Todos
- set a clear, well-defined and described functions for each step or operation, in 
order to be able to easily make the changes later
- add the depot as the first and the last node in the Route.route, or just consider it in the evaluate function (add them as arguments)
- documentation, diagrams: class and sequence, sample map (repere)
- consider the capacity of each vehicle
## Issues
- we had to make a deepcopy on the current_sol object in `switch_customers_in_solution()`, in order to keep the initial one intact 