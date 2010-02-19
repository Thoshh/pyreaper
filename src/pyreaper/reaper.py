'''
@author: pcarranza@gmail.com
'''
import sys
import os.path

from cleaner import Cleaner
from optparse import OptionParser
from browser import Walker


def main():
    parser = OptionParser(usage="%prog [options] <path to folder> <path to folder...>")
    parser.add_option("-e", 
                      "--ext", 
                      dest="extension", 
                      action="store",
                      help="only applies to the given extension" )
    parser.add_option("-s",
                      "--store-hashes",
                      dest="storehash",
                      action="store_true",
                      help="store calculated hashes in .digest hidden files")
    parser.add_option("-v",
                      "--verbose",
                      dest="verbose",
                      action="store_true",
                      help="outputs much more information during process, " + 
                      "sometimes even too much")
    parser.add_option("",
                      "--ignore-stored-hashes",
                      dest="ignorehashes",
                      action="store_true",
                      help="ignores stored calculated hashes in .digest " + 
                      "hidden files, this means every hash will be " + 
                      "recalculated")
    parser.add_option("-i",
                      "--interactive",
                      dest="interactive",
                      action="store_true",
                      help="interactive mode, will ask for each duplicate")
    
    (options, args) = parser.parse_args()

    if not args:
        parser.print_help()
        sys.exit(1)
    
    br = Walker(options.extension, \
			options.storehash, \
			options.verbose, \
			options.ignorehashes)
    
    for path in args:
        if not os.path.exists(path):
            parser.print_help()
            print "path {0} does not exists".format(path)
            sys.exit(1)
            
        br.digest(path)
    
    duplicates = br.getCollisions()
    if duplicates:
        print "Duplicates found..."
        c = Cleaner(duplicates, \
                    options.interactive, \
                    options.verbose)
        if c.clean():
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        print "No duplicates found"
        
    sys.exit(0)


if __name__ == '__main__':
    main()

