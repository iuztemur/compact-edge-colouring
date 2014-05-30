import pprint
import operator
import itertools

from collections import Counter

from opener import read_graph_from_file

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_compact(node_colouring):
    """Check if given colouring for node is compact.
    """
    node_colouring2 = {k: v for k, v in node_colouring.items() if v != None}
    if len(node_colouring) in [0, 1]:
        return True
    range_start = min(node_colouring2.values())
    expected_range = range(range_start, range_start \
                                + len(node_colouring.values()))
    return all(colour in expected_range for colour in node_colouring.values())

def format_colouring(colouring):
    """Put nodes in edges signatures within colouring in alphabetic order.
    """
    return {tuple(sorted(key)): colouring[key] for key in colouring}

def format_edges(edges):
    """Put nodes in edges signatures in alphabetic order.
    """
    return [tuple(sorted(edge)) for edge in edges]

def init_nodes(graph):
    """Form list of graph nodes sorted by degrees.
    """
    nodes = graph.nodes()
    degrees = [graph.degree(node) for node in nodes]
    sorted_by_degrees = [node for (degree, node) \
                in sorted(zip(degrees, nodes), reverse=True)]
    return sorted_by_degrees

def edges_remaining(graph, colouring):
    """Count edges yet to be coloured for each node. Put the counts in dict.
    """
    c0 = Counter(elem[0] for elem in colouring.keys())
    c1 = Counter(elem[1] for elem in colouring.keys())
    return {node: graph.degree(node) - c0[node] - c1[node] \
                    for node in graph.nodes()}

def nodes_remaining(graph, edges_remaining):
    """Form list of nodes sorted by adjacent edges yet to be coloured 
       with 0 values excluded.
    """
    nodes_remaining = [node for node in graph.nodes() \
                            if edges_remaining[node] > 0]
    nodes_remaining.sort(key = lambda x : edges_remaining[x])
    return nodes_remaining

def node_colouring(graph, colouring, node):
    """Form dict representation of colouring adjacent to given node. 
       None for not coloured yet.
    """
    node_colouring = {}
    for edge in format_edges(graph.edges(node)):
        if edge in colouring:
            node_colouring[edge] = colouring[edge]
        else:
            node_colouring[edge] = None
    return node_colouring

def has_duplicates(d):
    return len(d) != len(set(d.values()))

def possible_compact(node_colours):
    """Check if compact colouring is still possible for node.
    """
    no_of_edges = len(node_colours)
    node_colours = {k: v for k, v in node_colours.items() if v != None}
    if len(node_colours) == 0:
        return True
    if has_duplicates(node_colours):
        return False
    max_colour = max(node_colours.values())
    min_colour = min(node_colours.values())
    possible = max_colour - min_colour < no_of_edges
    logger.debug('possible_compact() %s', possible)
    return possible

def gap_to_fill(node_colours):
    """Identify colours needed to fill the interval.
    """
    node_colours = {k: v for k, v in node_colours.items() if v != None}
    max_colour = max(node_colours.values())
    min_colour = min(node_colours.values())
    return [c for c in range(min_colour + 1, max_colour) \
                if c not in node_colours.values()]

def none_edges(node_colours):
    """Form list of edges yet to be coloured for node.
    """
    return [k for k,v in node_colours.items() if v == None]

def min_edge_colour(node_colours):
    """Identify current minimum in colouring for node.
    """
    node_colours = {k: v for k, v in node_colours.items() if v != None}
    return min(node_colours.values())

def max_edge_colour(node_colours):
    """Identify current maximum in colouring for node.
    """
    node_colours = {k: v for k, v in node_colours.items() if v != None}
    return max(node_colours.values())

def surrounding(node_colours, gapping):
    """Identify options available apart from completing the interval.

    Say we have colouring for node: [2, 4, None, None, None]. These goes for
    2 edges with colours already assigned and 3 yet to be coloured. First,
    we need to complement the interval: [2, 3, 4] and we need 1 edge for that
    which in turn leaves us with 2 edges yet to be coloured. They can extend
    the interval in a number of ways, like [0, 1, 2, 3, 4] or [1, 2, 3, 4, 5].

    The purpose of this function is to identify these possible extentions.
    """
    edges_for_surr = len(none_edges(node_colours)) - len(gapping)
    min_colour = min_edge_colour(node_colours)
    max_colour = max_edge_colour(node_colours)
    places_to_the_left = min(min_colour, edges_for_surr)
    places_to_the_right = edges_for_surr - places_to_the_left
    surrs = []
    while places_to_the_left >= 0:
        surr =  range(min_colour - places_to_the_left, min_colour)
        surr += range(max_colour + 1, \
                    max_colour + 1 + edges_for_surr - places_to_the_left)
        surrs.append(surr)
        places_to_the_left  -= 1
        places_to_the_right += 1
    return surrs

def remaining_colours(node_colours):
    """Identify possible sets of colours for the remaining edges.
    """
    gap = gap_to_fill(node_colours)
    surrs = surrounding(node_colours, gap)
    return [sorted(s + gap) for s in surrs]

def edges_to_colours_matchings(blanks, colours):
    """Identify all combinations for given bland edges and colours.
    """
    return [sorted(zip(x,colours)) for x in itertools.permutations(blanks)]

def edges_to_colours_ideas_matchings(blanks, colours_ideas):
    """Go through all ideas for colours and match them against blank edges.
    """
    edge_colour_pairs = []
    for colours_idea in colours_ideas:
        edge_colour_pairs += \
            edges_to_colours_matchings(blanks, colours_idea)
    return edge_colour_pairs

def edges_to_colours_ideas_matchings_as_dict(matchings_lists_list):
    """Convert colours to blank edges matches into list of dictionaries
       each being one matching.
    """
    matchings_dicts_list = []
    for matching_list in matchings_lists_list:
        matchings_dicts_list.append( \
            {x[0]: x[1] for x in matching_list})
    return matchings_dicts_list

def remaining_colourings(node_colours):
    """Get all possible colourings of remaining blank egdes.
    """
    blank_edges       = none_edges(node_colours)
    colours_ideas     = remaining_colours(node_colours)
    edge_colour_pairs = \
        edges_to_colours_ideas_matchings(blank_edges, colours_ideas)
    return edges_to_colours_ideas_matchings_as_dict(edge_colour_pairs)

def possibilities(graph, node):
    """Get all possible initial colourings for given node of highest degree.
    """
    edges = format_edges(graph.edges(node))
    colours = range(len(edges))
    logger.debug('Checking possibilities for node %s', node)
    logger.debug('Edges adjacent to node: %s', edges)
    logger.debug('Colours to be matched against those edges: %s', colours)
    possibilities = edges_to_colours_ideas_matchings_as_dict( \
                        edges_to_colours_ideas_matchings(edges, [colours]))
    logger.debug('Possibilities are:\n%s\n', pprint.pformat(possibilities))
    return possibilities

def those_nodes_can_be_compact(graph, colouring, those_nodes):
    logger.debug('those_nodes_can_be_compact()')
    for this_node in those_nodes:
        this_node_colours = node_colouring(graph, colouring, this_node)
        logger.debug('this_node_colours: %s', this_node_colours)
        if not possible_compact(this_node_colours):
            return False
    return True

class SearchNode:
    def __init__(self, colouring=None, prev=None):
        self.colouring = colouring
        self.prev      = prev
        self.children  = []

    def add_child(self, child):
        self.children.append(child)

    def possible_leaf_colourings(self, possibilities):
        self.possibilities = possibilities

    def pop_possibility(self):
        logger.debug('self.possibilities = %s', self.possibilities)
        if self.possibilities == []:
            return None
        possibility = self.possibilities[0]
        self.possibilities = self.possibilities[1:]
        logger.debug('Possibilities remaining:\n%s\n', \
                        pprint.pformat(self.possibilities))
        return possibility

    def current_colouring(self):
        logger.debug('current colouring()')
        colours = self.colouring
        logger.debug('self.colouring = %s', colours)
        node = self.prev
        while node.prev != None and node.colouring != None:
            logger.debug('node.colouring = %s', node.colouring)
            colours = dict(colours.items() + node.colouring.items())
            node = node.prev
        return colours

logger.info('Reading graph from file')

graph = read_graph_from_file('graph1')
nodes_by_degrees = init_nodes(graph)
logger.info('Nodes sorted by degrees: %s', \
    [(node, graph.degree(node)) for node in nodes_by_degrees])

current_search_node = SearchNode()
current_search_node.possible_leaf_colourings( \
                    possibilities(graph,nodes_by_degrees[0]))
logger.info('Inserted all possible node %s colourings into root Search Node', \
             nodes_by_degrees[0])

a = 100

while a > 0:
    logger.info('a = %s', a)

    next_possible_colouring = current_search_node.pop_possibility()
    logger.info('Next possible colouring: %s', \
                    pprint.pformat(next_possible_colouring))

    if next_possible_colouring == None:
        logger.info('No next possible colouring in Search Node')
        if current_search_node.prev == None:
            logger.info('This is where things come to an end')
            break
        current_search_node = current_search_node.prev
        logger.info('Going up in tree')
        a -= 1
        continue

    prev_search_node = current_search_node
    current_search_node = SearchNode(next_possible_colouring, prev_search_node)
    prev_search_node.add_child(current_search_node)
    logger.info('New Search Node added')

    colouring = current_search_node.current_colouring()
    logger.info('Current colouring: %s', colouring)

    if those_nodes_can_be_compact(graph, colouring, graph.nodes()):
        logger.info('Compact not violated')

        edges_left = edges_remaining(graph, colouring)
        nodes_left = nodes_remaining(graph, edges_left)

        if not nodes_left:
            logger.info('Colouring successful')
            break

        logger.info('Nodes sorted by remaining edges: %s', \
            pprint.pformat( [(node, edges_left[node])  \
                                    for node in nodes_left] ) )

        current_node = nodes_left[0]
        node_colours = node_colouring(graph, colouring, current_node)
        logger.info('Picking node %s: coloured %s', current_node, node_colours)

        possibilities = remaining_colourings(node_colours)
        current_search_node.possible_leaf_colourings(possibilities)
        logger.info('Possible colourings: %s', pprint.pformat(possibilities))
        logger.info('Inserted all possible node %s ' + \
                        'colourings into Search Node', current_node)
        logger.info('Going down in tree')
    else:
        logger.info('Compact violated')
        current_search_node = current_search_node.prev
        logger.info('Going up in tree')

    a -= 1
