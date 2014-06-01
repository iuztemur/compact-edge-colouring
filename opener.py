import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import networkx as nx
from pprint import pformat

def read_edges_from_file(path):
    graph_file = open(path)
    lines = graph_file.readlines()
    edges = [tuple(line.split()) for line in lines]
    logger.info("Graph read from file:\n%s", pformat(edges))
    return edges

def read_graph_from_file(path):
    G = nx.Graph()
    G.add_edges_from(read_edges_from_file(path))
    return G
