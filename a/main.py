from Problem import Problem
from a import breadth_first_tree_search, greedy_best_first_graph_search, uniform_cost_graph_search, astar_graph_search
from a import breadth_first_graph_search, depth_first_graph_search, depth_limited_graph_search, depth_first_tree_search
from a import depth_limited_tree_search, iterative_deepening_graph_search, iterative_deepening_tree_search, uniform_cost_tree_search
from a import greedy_best_first_tree_search, astar_tree_search

qa = Problem("Arad","Bucharest")

node = breadth_first_tree_search(qa)

# node = breadth_first_graph_search(qa)

# node = depth_first_graph_search(qa)

# node = depth_first_tree_search(qa)

# node = uniform_cost_graph_search(qa)

# node = uniform_cost_tree_search(qa)

# node = greedy_best_first_graph_search(qa)

# node = greedy_best_first_tree_search(qa)

# node = astar_graph_search(qa)

# node = astar_tree_search(qa)

# node = depth_limited_graph_search(qa)

# node = depth_limited_tree_search(qa)

# node = iterative_deepening_graph_search(qa)

# node = iterative_deepening_tree_search(qa) #error

if type(node) is str:
    print(node)
elif node is None:
    print("no answer")
else:
    print("path cost: " + str(node.path_cost) + "\ndepth: " + str(node.depth) +
          "\npath: " + str(node.path()) + "\nnumber of visited nodes : " + str(qa.get_visited()) +
          "\nnumber of expanded nodes : " + str(qa.get_expanded()) + "\nmax memory use: " + str(qa.get_mmu()))