from opener import read_graph_from_file
from collections import Counter

class SearchNode:
    def __init__(self, colouring=None, prev=None):
        self.colouring = colouring
        self.prev      = prev
        self.children  = []

    def add_child(self, child):
        self.children.append(child)

def is_compact(node_colouring):
    if len(node_colouring) in [0, 1]:
        return True
    range_start = min(node_colouring.values())
    expected_range = range(range_start, range_start + len(node_colouring.values()))
    return all(colour in expected_range for colour in node_colouring.values())

print 'just starting'

graph = read_graph_from_file('graph1')
nodes = graph.nodes()
degrees = [graph.degree(node) for node in nodes]
nodes_sorted_by_degrees = [node for (degree, node) in sorted(zip(degrees, nodes), reverse=True)]
print 'all nodes sorted by degrees:', nodes_sorted_by_degrees

# init decision tree
root_node = SearchNode()

# propose colouring for the first element in this list
edges = graph.edges(nodes_sorted_by_degrees[0])
colouring = {edge : edges.index(edge) for edge in edges}
print '\n1st colouring:', colouring

# add node to tree
current_search_node = SearchNode(colouring, root_node)
root_node.add_child(current_search_node)

# sort the rest of nodes by number of colours yet to be assigned
nodes_remaining = nodes_sorted_by_degrees[1:]
c0 = Counter(elem[0] for elem in colouring.keys())
c1 = Counter(elem[1] for elem in colouring.keys())
edges_remaining = {node : graph.degree(node) - c0[node] - c1[node] 
    for node in nodes_remaining}
print '\nremaining edges:', edges_remaining
nodes_remaining.sort(key = lambda x : edges_remaining[x])
print 'nodes sorted by number of edges yet to be coloured:'
print nodes_remaining

# check possible colouring for node with the smallest number 
# of colours yet to be assigned
current_node = nodes_remaining[0]
print '\ncurrently looking at node', current_node

