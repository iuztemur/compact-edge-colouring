import logging
logger = logging.getLogger(__name__)

import argparse
from pprint import pformat

def main(args):
    if args.debug:
        logger.info("Logging level set to DEBUG")
        logging.basicConfig(level=logging.DEBUG)
    import algorithm, printer # must be here for level to take effect

    colouring = algorithm.colour_graph(args.graph_file)
    logger.info("Result:\n%s", pformat(colouring))

    if args.output != None and colouring != None:
        printer.print_colouring(colouring, args.output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("graph_file", help="graph file")
    parser.add_argument("-o", "--output", help="colouring file")
    parser.add_argument("-d", "--debug", help="set logging level to debug", 
                        action="store_true")
    args = parser.parse_args()
    main(args)