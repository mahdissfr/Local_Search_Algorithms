
class Node:


    def __init__(self, state, color=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.color = color
        self.neighbor_list = []


    def set_color(self, c):
        self.color = c

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def add_neighbor(self, n_list):
        """List the nodes reachable in one step from this node."""
        self.neighbor_list.extend(n_list)
        return self.neighbor_list


    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)


