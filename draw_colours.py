import logging
logger = logging.getLogger(__name__)

import networkx as nx
import pylab

from pprint import pformat

def from_colouring(colouring):
    graph = nx.Graph()
    graph.add_edges_from(colouring.keys())
    logger.debug("graph.edges() = \n%s", pformat(graph.edges()))

    pos = nx.spring_layout(graph)
    pylab.figure(1)
    nx.draw(graph,pos)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=colouring)
    pylab.show()

def from_file(colouring_file):
    with open(colouring_file) as f:
        colouring = {(line.split()[0], line.split()[1]): int(line.split()[2]) for line in f}
    logger.debug("colouring = \n%s", pformat(colouring))

    from_colouring(colouring)
    