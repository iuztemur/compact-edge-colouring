import logging
logger = logging.getLogger(__name__)

import pprint

def print_colouring(colouring, colouring_file):
    logger.info("Writing colouring to file '%s'", colouring_file)
    f = open(colouring_file, 'w')

    for key in colouring:
        f.write(key[0] + ' ' + key[1] + ' ' + str(colouring[key]) + '\n')

    f.close()
