"""Search (Chapters 3-4)
The way to use this code is to subclass Problem to create a class of problems,
then create problem instances and solve them with calls to the various search
functions."""
from collections import deque
from Problem import heuristics, edges, get_gn
from Node import Node

infinity = float('inf')
# ______________________________________________________________________________
# breadth first search

def breadth_first_tree_search(problem):
    """Search the shallowest nodes in the search tree first.
        Search through the successors of a problem to find a goal.
        The argument frontier should be an empty queue.
        Repeats infinitely in case of loops. [Figure 3.7]"""
    problem.reset_visited()
    problem.reset_expanded()
    problem.reset_mmu()
    frontier = deque([Node(problem.initial)])  # FIFO queue
    problem.update_mmu(len(frontier))
    while frontier:
        node = frontier.popleft()
        problem.inc_visited()
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
        problem.update_mmu(len(frontier))
    return None

def breadth_first_graph_search(problem):
    """[Figure 3.11]
    Note that this function can be implemented in a
    single line as below:
    return graph_search(problem, FIFOQueue())
    """
    problem.reset_visited()
    problem.reset_expanded()
    problem.reset_mmu()
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    frontier = deque([node])
    explored = set()
    problem.update_mmu(len(frontier) + len(explored))
    while frontier:
        node = frontier.popleft()
        problem.inc_visited()
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                if problem.goal_test(child.state):
                    return child
                frontier.append(child)
        problem.update_mmu(len(frontier) + len(explored))
    return None

# ______________________________________________________________________________
# depth first search

def depth_first_tree_search(problem):
    """Search the deepest nodes in the search tree first.
        Search through the successors of a problem to find a goal.
        The argument frontier should be an empty queue.
        Repeats infinitely in case of loops. [Figure 3.7]"""
    problem.reset_visited()
    problem.reset_expanded()
    problem.reset_mmu()
    frontier = [Node(problem.initial)]  # Stack
    problem.update_mmu(len(frontier))
    while frontier:
        node = frontier.pop()
        problem.inc_visited()
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
        problem.update_mmu(len(frontier))
    return None


def depth_first_graph_search(problem):
    """Search the deepest nodes in the search tree first.
        Search through the successors of a problem to find a goal.
        The argument frontier should be an empty queue.
        Does not get trapped by loops.
        If two paths reach a state, only use the first one. [Figure 3.7]"""
    problem.reset_visited()
    problem.reset_expanded()
    problem.reset_mmu()
    frontier = [(Node(problem.initial))]  # Stack
    explored = set()
    problem.update_mmu(len(frontier) + len(explored))
    while frontier:
        node = frontier.pop()
        problem.inc_visited()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        frontier.extend(child for child in node.expand(problem)
                        if child.state not in explored and
                        child not in frontier)
        problem.update_mmu(len(frontier) + len(explored))
    return None

def depth_limited_tree_search(problem, limit=len(edges)):
    problem.reset_visited()
    problem.reset_expanded()
    problem.reset_mmu()
    frontier = [Node(problem.initial)]  # Stack
    problem.update_mmu(len(frontier))
    lmt=limit
    while frontier and lmt != 0:
        lmt -= 1
        node = frontier.pop()
        problem.inc_visited()
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
        problem.update_mmu(len(frontier))
    if lmt == 0:
        return 'cutoff'
    else:
        return None

def depth_limited_graph_search(problem, limit=len(edges)):

    problem.reset_visited()
    problem.reset_expanded()
    problem.reset_mmu()
    frontier = [(Node(problem.initial))]  # Stack
    explored = set()
    problem.update_mmu(len(frontier) + len(explored))
    lmt = limit
    while frontier and lmt != 0:
        lmt -= 1
        node = frontier.pop()
        problem.inc_visited()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        frontier.extend(child for child in node.expand(problem)
                        if child.state not in explored and
                        child not in frontier)
        problem.update_mmu(len(frontier) + len(explored))
    if lmt == 0:
        return 'cutoff'
    else:
        return None


def iterative_deepening_tree_search(problem):
    problem.reset_visited()
    problem.reset_expanded()
    dlgs_xpnd_keeper = 0
    dlgs_vztd_keeper = 0
    for depth in range(0, len(edges)):
        result = depth_limited_tree_search(problem, depth)
        dlgs_xpnd_keeper += problem.get_expanded()
        dlgs_vztd_keeper += problem.get_visited()
        if result != 'cutoff':
            problem.update_expanded(dlgs_xpnd_keeper)
            problem.update_expanded(dlgs_vztd_keeper)
            return result

def iterative_deepening_graph_search(problem):
    problem.reset_visited()
    problem.reset_expanded()
    dlgs_xpnd_keeper = 0
    dlgs_vztd_keeper = 0
    for depth in range(0, len(edges)):
        result = depth_limited_graph_search(problem, depth)
        dlgs_xpnd_keeper += problem.get_expanded()
        dlgs_vztd_keeper += problem.get_visited()
        if result != 'cutoff':
            problem.update_expanded(dlgs_xpnd_keeper)
            problem.update_expanded(dlgs_vztd_keeper)
            return result

# ______________________________________________________________________________
# uniform cost search

def same_state(frontier, state):

    for node_g in frontier:
        if node_g[0].state == state:
            return node_g[0]
    return None


def Sort_frontier(sub_li):

    l = len(sub_li)
    for i in range(0, l):
        for j in range(0, l-i-1):
            if (sub_li[j][1] > sub_li[j + 1][1]):
                tempo = sub_li[j]
                sub_li[j]= sub_li[j + 1]
                sub_li[j + 1]= tempo
    return sub_li

def uniform_cost_graph_search(problem):

    problem.reset_visited()
    problem.reset_expanded()
    problem.reset_mmu()
    frontier = [[Node(problem.initial), Node(problem.initial).path_cost]]
    explored = []
    problem.update_mmu(len(frontier) + len(explored))
    while frontier:
        Sort_frontier(frontier)
        (node, g) = frontier.pop(0)
        problem.inc_visited()
        if problem.goal_test(node.state):
            return node
        explored.append(node.state)
        for child in node.expand(problem):
            ss = same_state(frontier, child.state)
            if child.state not in explored and child not in frontier:
                frontier.append([child, child.path_cost])
            elif ss is not None:
                if ss.path_cost > child.path_cost:
                    frontier.remove([ss, ss.path_cost])
                    frontier.append([child, child.path_cost])
            problem.update_mmu(len(frontier) + len(explored))
    return None


def uniform_cost_tree_search(problem):
    problem.reset_visited()
    problem.reset_expanded()
    problem.reset_mmu()
    frontier = [[Node(problem.initial), Node(problem.initial).path_cost]]
    problem.update_mmu(len(frontier))
    while frontier:
        Sort_frontier(frontier)
        (node, g) = frontier.pop()
        problem.inc_visited()
        if problem.goal_test(node.state):
            return node
        for child in node.expand(problem):
            ss = same_state(frontier, child.state)
            if child not in frontier:
                frontier.append([child, child.path_cost])
            elif ss is not None:
                if get_gn(ss) > get_gn(child):
                    frontier.remove([ss, ss.path_cost])
                    frontier.append([child, child.path_cost])
            problem.update_mmu(len(frontier))
    return None

# ______________________________________________________________________________
# Best First Graph search
def greedy_best_first_graph_search(problem):
    problem.reset_visited()
    problem.reset_mmu()
    problem.reset_expanded()
    frontier = [[Node(problem.initial),heuristics[problem.initial]]]
    explored = set()
    problem.update_mmu(len(frontier) + len(explored))
    while frontier:
        # frontier = sorted(frontier, key = lambda x: x[1])
        Sort_frontier(frontier)
        (node, h) = frontier.pop()
        problem.inc_visited()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append([child, heuristics[child.state]])
        problem.update_mmu(len(frontier) + len(explored))
    return None

def greedy_best_first_tree_search(problem):
    problem.reset_visited()
    problem.reset_expanded()
    problem.reset_mmu()
    frontier = [[Node(problem.initial), heuristics[problem.initial]]]
    problem.update_mmu(len(frontier))
    while frontier:
        Sort_frontier(frontier)
        (node, h) = frontier.pop()
        problem.inc_visited()
        if problem.goal_test(node.state):
            return node
        for child in node.expand(problem):
            if child not in frontier:
                frontier.append([child, heuristics[child.state]])
        problem.update_mmu(len(frontier))
    return None



# Greedy best-first search is accomplished by specifying f(n) = h(n).

# ______________________________________________________________________________
# Astar
def astar_graph_search(problem):
    problem.reset_visited()
    problem.reset_expanded()
    problem.reset_mmu()
    frontier = [[Node(problem.initial), Node(problem.initial).path_cost + heuristics[problem.initial] ]]
    explored = set()
    problem.update_mmu(len(frontier) + len(explored))
    while frontier:
        Sort_frontier(frontier)
        (node, pc) = frontier.pop()
        problem.inc_visited()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            ss = same_state(frontier, child.state)
            if child.state not in explored and child not in frontier:
                frontier.append([child, child.path_cost + heuristics[child.state] ])
            elif ss is not None:
                if ( ss.path_cost + heuristics[ss.state] ) > ( child.path_cost + heuristics[child.state] ):
                    frontier.remove([ss, ss.path_cost])
                    frontier.append([child, child.path_cost] + + heuristics[child.state] )
            problem.update_mmu(len(frontier) + len(explored))
    return None

def astar_tree_search(problem):
    problem.reset_visited()
    problem.reset_expanded()
    problem.reset_mmu()
    frontier = [[Node(problem.initial), Node(problem.initial).path_cost + heuristics[problem.initial]]]
    problem.update_mmu(len(frontier))
    while frontier:
        Sort_frontier(frontier)
        (node, pc) = frontier.pop()
        problem.inc_visited()
        if problem.goal_test(node.state):
            return node
        for child in node.expand(problem):
            ss = same_state(frontier, child.state)
            if child not in frontier:
                frontier.append([child, child.path_cost + heuristics[child.state]])
            elif ss is not None:
                if get_gn(ss) > get_gn(child):
                    frontier.remove([ss, ss.path_cost])
                    frontier.append([child, child.path_cost] + + heuristics[child.state])
            problem.update_mmu(len(frontier))
    return None

