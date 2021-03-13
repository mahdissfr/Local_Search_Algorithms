
import random
from Problem import Problem
import numpy
import copy
from matplotlib import pyplot as plt


def new_population_production(populationSize):
    population = []
    for i in range(0, populationSize):
        chromosome = Problem()
        for node in chromosome.graph:
            node.set_color(random.choice([0, 1, 2]))
        population.append(chromosome)
    return population

def best_fitness(tornument):
    tmp = []
    for chromosome in tornument:
        tmp.append([chromosome,chromosome.fitness()])
    if len(tmp) != 0:
        return Sort_list(tmp).pop()[0]
    return None

def Sort_list(sub_li): #Ascending
    l = len(sub_li)
    for i in range(0, l):
        for j in range(0, l-i-1):
            if (sub_li[j][1] > sub_li[j + 1][1]):
                tempo = sub_li[j]
                sub_li[j]= sub_li[j + 1]
                sub_li[j + 1]= tempo
    return sub_li

def k_random_choice(population, tornument_nom, tornumentSize):
    pop_copy = copy.deepcopy(population)
    selected_parent = []
    tornument = []
    for i in range(0, tornument_nom):
        for j in range(0, tornumentSize):
            chromosome = random.choice(pop_copy)
            pop_copy.remove(chromosome)
            tornument.append(chromosome)
        selected_parent.append(best_fitness(tornument))
    return selected_parent


def parent_selection(tornumentSize, population):
    tornument_nom = int(len(population)/tornumentSize)
    return k_random_choice(population, tornument_nom, tornumentSize)

def crossover(p1, p2, k=5):
    new_node = []
    for i in range(0, k):
        new_node.append(random.choice(p2.graph))
    for node in new_node:
        p1.reset_nodes_color(node.state, node.color)
    return p1

def new_generation(population, tornumentSize):
    new_chromosome = []
    while 1:
        selected_parent = parent_selection(tornumentSize, population)
        for i in range(0, len(selected_parent)):
            p1 = random.choice(selected_parent)
            p2 = random.choice(selected_parent)
            if p1 != p2:
                new_chromosome.append(crossover(p1, p2))
            if len(new_chromosome) == len(population):
                return new_chromosome



def mutation(population, mutationRate):
    mutatedGenomes = int(len(population) * 11 * mutationRate)
    for i in range(0, mutatedGenomes):
        chromosome = random.choice(population)
        random.choice(chromosome.graph).set_color(random.choice([0, 1, 2]))
    return population

def per_generation_fitness(population):
    fitness_list = []
    for graph in population:
        fitness_list.append(graph.fitness())
    return fitness_list

def max_min_avg_fitness(list):
    max = 0
    min = float('inf')
    sum = 0
    for i in range(0, len(list)):
        if list[i] < min:
            min = list[i]
        if list[i] > max:
            max = list[i]
        sum += list[i]
    return [max, min, sum/len(list)]


def diagram(generations_fitness_list):
    max_list = []
    min_list = []
    avg_list = []
    for j in range(0, len(generations_fitness_list)):
        tmp = max_min_avg_fitness(generations_fitness_list[j])
        max_list.append(tmp[0])
        min_list.append(tmp[1])
        avg_list.append(tmp[2])
        print("generation number " + str(j) + " : " + "\nbest fitness : "
              + str(max_list[j]) + "\nworst fitness : " + str(min_list[j]) +
              "\naverage fitness : " + str(avg_list[j]))
    x = range(len(generations_fitness_list))
    plt.scatter(x, max_list)
    plt.show()
    plt.scatter(x, min_list)
    plt.show()
    plt.scatter(x, avg_list)
    plt.show()


def gen_goal_test(generation):
    for graph in generation:
        if graph.goal_test():
            return graph
    return None

def genetics(numberOfGenerations, populationSize, tornumentSize, mutationRate):
    counter=0
    generations_fitness_list = []
    population = new_population_production(populationSize)
    counter +=1
    gtest = gen_goal_test(population)
    if gtest is not None:
        return [gtest,counter]
    generations_fitness_list.append(per_generation_fitness(population))
    for i in range(0, numberOfGenerations):
        new_gen = new_generation(population, tornumentSize)
        counter += 1
        population[:] = []
        population = mutation(new_gen, mutationRate)
        gtest = gen_goal_test(population)
        if gtest is not None:
            return gtest
        generations_fitness_list.append(per_generation_fitness(population))
    diagram(generations_fitness_list)
    return None


#______________________________________
#simulated_annealing
def simulation_probability(xval, val, t):
    delta = val - xval
    return numpy.exp(delta/t)

def simulated_annealing(problem):
    current_state = problem
    current_val = current_state.value()
    temperature = 1
    t_min = 0.001
    alpha = 0.9
    while temperature > t_min:
        cntr=1
        while cntr <= 100:
            actions = current_state.action()
            neighbours = current_state.result(actions)
            current_state.inc_visited()
            new_state = random.choice(neighbours)
            new_val = new_state.value()
            p = simulation_probability(current_val, new_val, temperature)
            if p < numpy.random.uniform(0,1):
                current_state.inc_explored()
                new_state.set_explored(current_state.explored)
                new_state.set_visited(current_state.visited)
                current_state = new_state
                current_val = new_val
            cntr += 1
        temperature *= alpha
        return current_state
#_________________________________________________
# hill climbing


def best_value(neighbours):
    tmp = []
    for neighbour in neighbours:
        tmp.append([neighbour, neighbour.value()])
    return Sort_list(tmp).pop(0)


def hill_climbing(problem):
    current_state = problem
    while 1:
        actions = current_state.action()
        neighbours = current_state.result(actions)
        current_state.inc_visited()
        temp_best = best_value(neighbours)[0]
        if temp_best.value() >= current_state.value():
            return current_state
        current_state.inc_explored()
        temp_best.set_explored(current_state.explored)
        temp_best.set_visited(current_state.visited)
        current_state = temp_best


def better_value(neighbours, value):
    better = []
    for neighbour in neighbours:
        if neighbour.value() < value :
            better.append(neighbour)
    return better


def stochastic_hill_climbing(problem):
    current_state = problem
    while 1:
        actions = current_state.action()
        neighbours = current_state.result(actions)
        current_state.inc_visited()
        better = better_value(neighbours, current_state.value())
        if len(better) == 0:
            return current_state
        choosed = random.choice(better)
        current_state.inc_explored()
        choosed.set_explored(current_state.explored)
        choosed.set_visited(current_state.visited)
        current_state = choosed


def first_better_choice(neighbours, value):
    random.shuffle(neighbours)
    for neighbour in neighbours:
        if neighbour.value() < value:
            return neighbour
    return None


def first_choice_hill_climbing(problem):
    current_state = problem
    while 1:
        actions = current_state.action()
        neighbours = current_state.result(actions)
        current_state.inc_visited()
        fbc = first_better_choice(neighbours, current_state.value())
        if fbc is None:
            return current_state
        current_state.inc_explored()
        fbc.set_explored(current_state.explored)
        fbc.set_visited(current_state.visited)
        current_state = fbc


def random_restart_hill_climbing(n=100):
    current_state = hill_climbing(Problem().randomize_graph())
    best_val = current_state.value()
    visited = current_state.visited
    explored = current_state.explored
    for i in range(0, n-1):
        tmp = hill_climbing(Problem().randomize_graph())
        visited += tmp.visited
        explored += tmp.explored
        if tmp.value() < best_val:
            current_state = tmp
            best_val = current_state.value()
    current_state.set_explored(explored)
    current_state.set_visited(visited)
    return current_state

