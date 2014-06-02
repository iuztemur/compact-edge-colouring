import logging
logger = logging.getLogger(__name__)

import argparse
from pprint import pformat

def main(args):
    with open('compec.log', 'w'):
        pass

    if args.debug:
        logger.info("Logging level set to DEBUG")
        logging.basicConfig(filename='compec.log', level=logging.DEBUG)
    else:
        logger.info("Logging level set to INFO")
        logging.basicConfig(filename='compec.log', level=logging.INFO)

    import algorithm, printer, draw_colours
    # must be here for level to take effect

    colouring = algorithm.colour_graph(args.graph_file)
    logger.info("Result:\n%s", pformat(colouring))
    
    if colouring != None:
        print pformat(colouring)
    else:
        print 'could not find colouring for graph'

    if args.present and colouring != None:
        draw_colours.from_colouring(colouring)

    if args.output != None and colouring != None:
        printer.print_colouring(colouring, args.output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("graph_file", help="graph file")
    parser.add_argument("-o", "--output", 
                        help="colouring file")
    parser.add_argument("-d", "--debug", 
                        help="set logging level to debug", 
                        action="store_true")
    parser.add_argument("-p", "--present", 
                        help="present colouring in graphical form",
                        action="store_true")
    args = parser.parse_args()
    main(args)