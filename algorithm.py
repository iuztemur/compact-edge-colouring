from opener import read_graph_from_file

G = read_graph_from_file('graph1')
nodes = G.nodes()
print "nodes read from graph from file: ", nodes

degrees = [G.degree(node) for node in nodes]
print "nodes degrees: ", degrees

nodes_sorted_by_degrees = [node for (degree, node) in sorted(zip(degrees, nodes), reverse=True)]
print "nodes sorted: ", nodes_sorted_by_degrees

# init decision tree

# propose colouring of the 1st element from this list

# maybe a true decision tree could be used for sake of fiding the minimum colors number