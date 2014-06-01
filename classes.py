import logging
logger = logging.getLogger(__name__)

import pprint

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
