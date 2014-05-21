import networkx as nx

def read_edges_from_file(path):
    graph_file = open(path)
    lines = graph_file.readlines()
    edges = [tuple(line.split()) for line in lines]
    return edges

def read_graph_from_file(path):
    G = nx.Graph()
    G.add_edges_from(read_edges_from_file(path))
    return G

""" tests
print "edges read from file: ", read_edges_from_file('graph1')
print "graph read from file: ", read_graph_from_file('graph1').edges()
"""
