

def is_in(elt, seq):
    """Similar to (elt in seq), but compares with 'is', not '=='."""
    return any(x is elt for x in seq)


text_file = open("graph.txt", "r")
edges = text_file.read().split('\n')
text_file.close()

gn = dict()
with open("graph.txt") as ssg:
    for line in ssg:
       (s1, s2, g) = line.split(' ')
       gn[str(s1)+" "+str(s2)] = int(g)



def get_gn(node):
    print("parent : "+str(node.parent))
    print("state : "+str(node.state))
    if node.parent is None :
        return 0
    elif str(node.state)+" "+str(node.parent.state) in gn:
        return gn[str(node.state)+" "+str(node.parent.state)]
    elif str(node.parent.state)+" "+str(node.state) in gn:
        return gn[str(node.parent.state)+" "+str(node.state)]

heuristics = dict()
with open("heuristics.txt") as heuristic:
    for line in heuristic:
       (key, val) = line.split(' ')
       heuristics[key] = int(val)


class Problem(object):
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None, visited = 0, expanded = 0, mmu = 0):
        self.initial = initial
        self.goal = goal
        self.visited = visited
        self.expanded = expanded
        self.mmu = mmu

    def reset_expanded(self):
        self.expanded = 0

    def update_expanded(self,num):
        self.expanded += num

    def get_expanded(self):
        return self.expanded

    def reset_mmu(self):
        self.mmu = 0

    def update_mmu(self, new_value):
        if new_value > self.mmu:
            self.mmu = new_value

    def get_mmu(self):
        return self.mmu

    def reset_visited(self):
        self.visited = 0

    def update_visited(self, new_value):
        self.visited = new_value

    def inc_visited(self):
        self.visited += 1

    def get_visited(self):
        return self.visited

    def actions(self, state):

        actions = []
        for edge in edges:
            if state in edge:
                actions.append(edge)

        return actions

    def result(self, state, action):

        (s1, s2, g) = action.split(' ')
        if s1 == state :
            return s2
        elif s2 == state :
            return s1
        else:
            print("wrong action")

    def goal_test(self, state):
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        (s1, s2, g) = action.split(' ')
        return int(g) + c


