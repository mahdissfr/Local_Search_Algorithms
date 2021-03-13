from Node import Node
import copy
import random

class Problem():

    def __init__(self, visited = 0, explored = 0):
        self.graph = self.form_graph()
        self.node_no = len(self.graph)
        self.edge_no = self.get_edge_no()
        self.visited = visited
        self.explored = explored

    def get_edge_no(self):
        cntr = 0
        for node in self.graph:
            cntr += len(node.neighbor_list)
        return cntr/2


    def reset_nodes_color(self, state, color):
        for node in self.graph:
            if node.state == state:
                node.set_color(color)
        return self


    def randomize_graph(self):
        for node in self.graph:
            node.set_color(random.choice([0, 1, 2]))
        return self


    def form_graph(self):
        #define nodes
        n0 = Node("n0",0)
        n1 = Node("n1",0)
        n2 = Node("n2",0)
        n3 = Node("n3",0)
        n4 = Node("n4",0)
        n5 = Node("n5",0)
        n6 = Node("n6",0)
        n7 = Node("n7",0)
        n8 = Node("n8",0)
        n9 = Node("n9",0)
        n10 = Node("n10",0)
        #add neghbors
        n0.add_neighbor([n1, n2, n3, n4, n5])
        n1.add_neighbor([n0, n6, n10])
        n2.add_neighbor([n0, n6, n7])
        n3.add_neighbor([n0, n7, n8])
        n4.add_neighbor([n0, n8, n9])
        n5.add_neighbor([n0, n9, n10])
        n6.add_neighbor([n1, n2, n8, n9])
        n7.add_neighbor([n2, n3, n9, n10])
        n8.add_neighbor([n3, n4, n6, n10])
        n9.add_neighbor([n4, n5, n6, n7])
        n10.add_neighbor([n1, n5, n7, n8])
        return [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10]

    def fitness(self):
        cntr = 0
        for node in self.graph:
            for neighbor in node.neighbor_list:
                if node.color != neighbor.color:
                    cntr += 1
        return cntr/self.edge_no

    def value(self):
        cntr = 0
        for node in self.graph:
            for neighbor in node.neighbor_list:
                if node.color == neighbor.color:
                    cntr += 1
        return int(cntr/2)

    def set_explored(self, num):
        self.explored = num

    def inc_explored(self):
        self.explored += 1

    def set_visited(self, num):
        self.visited = num

    def inc_visited(self):
        self.visited += 12

    def action(self):
        actions = []
        for node in self.graph:
            colors=[0,1,2]
            colors.pop(node.color)
            actions.append([node.state,colors])
        return actions

    def result(self, actions):
        population = []
        for action in actions:
            neighbor = copy.deepcopy(self)
            population.append(neighbor.reset_nodes_color(action[0],action[1][0]))
            population.append(neighbor.reset_nodes_color(action[0],action[1][1]))
        return population

    def goal_test(self):
        return self.value() == 0

    def solution(self):
        solution = []
        for node in self.graph:
            solution.append([node.state,node.color])
        return solution






