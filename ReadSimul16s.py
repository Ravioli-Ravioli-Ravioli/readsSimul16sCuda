#/bin/env python

import getopt
import sys
import os
//Test
def main(argv):
    # check arguments and options
    try:
        opts, args = getopt.getopt(argv, "hd:", ["help", "database"])
        # show usage printout if something is bad
        for opt, arg in opts:
            if opt in ("-h, --help"):
                printUsage()
                sys.exit(2)
            if opt in ("-d, --db"):
                print "Supposed to create db '" + arg +"'"
        MAIN_PROGRAM_METHOD(args[0])
    except getopt.GetoptError:
        printUsage(True)
        sys.exit(2)
    except IndexError:
        printUsage(True)
        sys.exit(2)

def printUsage(error = False):
    if error:
        print "Unknown option or missing argument."
    print """
    Usage: scriptname.py [options] <xml file>

    -h              show this help
    -d              use specific database
    """

if __name__ == "__main__":
    main(sys.argv[1:])
