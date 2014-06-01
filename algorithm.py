import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import pprint
from opener import read_graph_from_file

import steps

from classes import SearchNode

def colour_graph(graph_file_path):

    graph = read_graph_from_file(graph_file_path)
    nodes_by_degrees = steps.init_nodes(graph)
    logger.debug('Nodes sorted by degrees:\n%s', \
        pprint.pformat([(node, graph.degree(node)) 
                            for node in nodes_by_degrees]))

    current_search_node = SearchNode()
    current_search_node.possible_leaf_colourings( \
                        steps.possibilities(graph,nodes_by_degrees[0]))
    logger.debug('Inserted all possible node %s colourings into root Search Node', \
                 nodes_by_degrees[0])

    while True:
        next_possible_colouring = current_search_node.pop_possibility()
        logger.debug('Next possible colouring:\n%s', \
                        pprint.pformat(next_possible_colouring))

        if next_possible_colouring == None:
            logger.debug('No next possible colouring in Search Node')
            if current_search_node.prev == None:
                logger.info('Could not find graph colouring')
                return None
            current_search_node = current_search_node.prev
            logger.debug('Going up in tree')
            continue

        prev_search_node = current_search_node
        current_search_node = \
                SearchNode(next_possible_colouring, prev_search_node)
        prev_search_node.add_child(current_search_node)
        logger.debug('New Search Node added')

        colouring = current_search_node.current_colouring()
        logger.debug('Current colouring:\n%s', pprint.pformat(colouring))

        if steps.those_nodes_can_be_compact(graph, colouring, graph.nodes()):
            logger.debug('Compact not violated')

            edges_left = steps.edges_remaining(graph, colouring)
            nodes_left = steps.nodes_remaining(graph, edges_left)

            if not nodes_left:
                logger.info('Colouring successful')
                return colouring

            logger.debug('Nodes sorted by remaining edges:\n%s', \
                pprint.pformat( [(node, edges_left[node])  \
                                        for node in nodes_left] ) )

            current_node = nodes_left[0]
            node_colours = steps.node_colouring(graph, colouring, current_node)
            logger.debug('Picking node %s coloured:\n%s',
                            current_node, node_colours)

            possibilities = steps.remaining_colourings(node_colours)
            current_search_node.possible_leaf_colourings(possibilities)
            logger.debug('Possible colourings:\n%s', 
                                pprint.pformat(possibilities))
            logger.debug('Inserted all possible node %s ' + \
                            'colourings into Search Node', current_node)
            logger.debug('Going down in tree')
        else:
            logger.debug('Compact violated')
            current_search_node = current_search_node.prev
            logger.debug('Going up in tree')
