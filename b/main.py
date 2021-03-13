
from search import genetics
from search import simulated_annealing, hill_climbing, stochastic_hill_climbing, first_choice_hill_climbing, random_restart_hill_climbing
from Problem import Problem
population = genetics(10, 100, 4, 0.2)
if type(population) is list:
    print("solution : ")
    print(population[0].solution())
    print("number of produced generations : "+ str(population[1]))

# qb = Problem()


# graph = simulated_annealing(qb)


# graph = hill_climbing(qb)


# graph = first_choice_hill_climbing(qb)


# graph = stochastic_hill_climbing(qb)


graph = random_restart_hill_climbing()


# print("number of visited nodes : " + str(graph.visited) + "\nnumber of explored nodes : " + str(graph.explored)+ "\nsolution : ")
# print(graph.solution())
# print("value : " + str(graph.value()))