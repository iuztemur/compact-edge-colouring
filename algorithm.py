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

def format_colouring(colouring):
    return {tuple(sorted(key)) : colouring[key] for key in colouring}

def format_edges(edges):
    return [tuple(sorted(edge)) for edge in edges]

def init_nodes(graph):
    nodes = graph.nodes()
    degrees = [graph.degree(node) for node in nodes]
    sorted_by_degrees = [node for (degree, node) in sorted(zip(degrees, nodes), reverse=True)]
    return sorted_by_degrees

def edges_remaining(graph, colouring):
    c0 = Counter(elem[0] for elem in colouring.keys())
    c1 = Counter(elem[1] for elem in colouring.keys())
    return {node: graph.degree(node) - c0[node] - c1[node] for node in graph.nodes()}

def nodes_remaining(graph, edges_remaining):
    nodes_remaining = [node for node in graph.nodes() if edges_remaining[node] > 0]
    nodes_remaining.sort(key = lambda x : edges_remaining[x])
    return nodes_remaining

def node_colouring(graph, colouring, node):
    node_colouring = {}
    for edge in format_edges(graph.edges(node)):
        if edge in colouring:
            node_colouring[edge] = colouring[edge]
        else:
            node_colouring[edge] = None
    return node_colouring

graph = read_graph_from_file('graph1')
nodes = init_nodes(graph)
print '0. nodes sorted by degrees'
print [(node, graph.degree(node)) for node in nodes]

root_search_node = SearchNode()

edges = graph.edges(nodes[0])
colouring = format_colouring({edge: edges.index(edge) for edge in edges})
print '\n1. colouring'
print colouring

current_search_node = SearchNode(colouring, root_search_node)
root_search_node.add_child(current_search_node)
print 'added as leaf'

edges_remaining = edges_remaining(graph, colouring)
nodes_remaining = nodes_remaining(graph, edges_remaining)
print '\nnodes sorted by remaining edges'
print [(node, edges_remaining[node]) for node in nodes_remaining]

current_node = nodes_remaining[0]
print 'pick', current_node
node_colours = node_colouring(graph, colouring, current_node)
print 'colours:', node_colours

# propose colouring for current node

print 
