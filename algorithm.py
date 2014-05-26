from opener import read_graph_from_file
from collections import Counter
from pprint import pprint
import operator

class SearchNode:
    def __init__(self, colouring=None, prev=None):
        self.colouring = colouring
        self.prev      = prev
        self.children  = []

    def add_child(self, child):
        self.children.append(child)

def is_compact(node_colouring):
    node_colouring = {k: v for k, v in node_colouring.items() if v != None}
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

def possible_compact(node_colours):
    no_of_edges = len(node_colours)
    node_colours = {k: v for k, v in node_colours.items() if v != None}
    max_colour = max(node_colours.values())
    min_colour = min(node_colours.values())
    return max_colour - min_colour < no_of_edges

graph = read_graph_from_file('graph1')
nodes = init_nodes(graph)
print '\n0. nodes sorted by degrees'
print [(node, graph.degree(node)) for node in nodes]

root_search_node = SearchNode()

edges = format_edges(graph.edges(nodes[0]))
colouring = {edge: edges.index(edge) for edge in edges}
print '\n1. colouring'
pprint(colouring)

current_search_node = SearchNode(colouring, root_search_node)
root_search_node.add_child(current_search_node)
print 'added as leaf'

edges_remaining = edges_remaining(graph, colouring)
nodes_remaining = nodes_remaining(graph, edges_remaining)
print '\nnodes sorted by remaining edges'
print [(node, edges_remaining[node]) for node in nodes_remaining]

current_node = nodes_remaining[0]
node_colours = node_colouring(graph, colouring, current_node)
print 'picking', current_node, '- coloured', node_colours
compact = 'yes' if is_compact(node_colours) else 'no'
print 'compact?', compact
possible = possible_compact(node_colours)
print 'possible?', possible

# propose colouring for current node

print 
