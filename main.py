from tabu import *

# VARIABLES
T = [] # tabu list: contains the list of changes
TT = 4 # tabu tenure: max number of the same change allowed
NUM_NEIGHBORS = 4 # the number of neighbors to search for on each iteration
num_iterations = 1000 # the number of iterations of the algorithm = num of total solutions discovered

if __name__ == "__main__":
  # BEGIN
  current = generate_random_solution()
  bst = current  # the best solution: to consider in the end
  while num_iterations > 0:
    neighbor_sols = generate_neighbor_solutions(current, NUM_NEIGHBORS, T)
    current1 = best(allowed(neighbor_sols, T, TT))
    if evaluate(current1) > evaluate(current):
      print("-----> ASPIRATION")
      # current1 is not better than current - We'll use the Aspiration Criteria (choosing from all of them, even non-allowed ones)
      current = best_from_sol_change_pairs(neighbor_sols)
    else:
      current = current1
    bst = min([bst, current], key=lambda sol: evaluate(sol))
    # print("--------------------- NEIGHBOR SOLUTIONS ---------------------")
    # for sol in neighbor_sols:
    #   print("======= NEIGHBOR SOLUTION ====")
    #   for route in sol.solution.routes:
    #     print(route)
    # print("--------------------------------------------------------------")
    print("CURRENT", 5000 - num_iterations, "=>", evaluate(current))
    print("BEST SOLUTION", 5000 - num_iterations, "=>", bst.cost)
    num_iterations -= 1

  # END

  for route in bst.routes:
    print(route)
  print("EVALUATION: ", bst.cost)
  print("TABU LIST=", T[0:5])