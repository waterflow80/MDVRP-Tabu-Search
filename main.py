from tabu import *
from time import time
# CONSTS
DATA_DIR = 'data/p' # The folder where all the test instances are located

# VARIABLES
T = [] # tabu list: contains the list of changes
TT = 4 # tabu tenure: max number of the same change allowed
NUM_NEIGHBORS = 30 # the number of neighbors to search for on each iteration
NUM_ITERATIONS = 1000 # the number of iterations of the algorithm = num of total solutions discovered
MAX_LIVING_CHANGE = 30

if __name__ == "__main__":
  start_time = time()
  # BEGIN
  for i in range(1, 2): # looping over the test instances under data/p*.txt
    count = 0 # for the display only
    #print("ITERATION N°",i)
    T = TabuListQueue(max_living_change=MAX_LIVING_CHANGE)
    num_iterations = NUM_ITERATIONS
    #print("--> Generating random solution")
    current = generate_random_solution(DATA_DIR + str(i) + '.txt', True)
    #print("--> FINISHED: Generating random solution")
    bst = current  # the best solution: to consider in the end
    while num_iterations > 0:
      neighbor_sols = generate_neighbor_solutions(current, NUM_NEIGHBORS, T)
      neighbor_solutions = list(map(lambda x: x.solution, neighbor_sols))
      current1 = best(neighbor_solutions)
      if evaluate(current1) > evaluate(current):
        #print("-----> ASPIRATION")
        # current1 is not better than current - We'll use the Aspiration Criteria (choosing from all of them, even non-allowed ones)
        current = best_from_sol_change_pairs(neighbor_sols)
      else:
        current = current1
      bst = min([bst, current], key=lambda sol: evaluate(sol))
      #print("CURRENT", count, "=>", evaluate(current))
      #print("BEST SOLUTION", count, "=>", bst.cost)
      num_iterations -= 1
      count += 1

  # END
    print("====================== " + DATA_DIR + str(i) + '.txt' + " ==================")
    # for route in bst.routes:
    #   print(route)
    print("BEST EVALUATION: ", bst.cost)
    print("===================================================")
  end_time = time()
  print("Total execution time:", end_time - start_time, " seconds")