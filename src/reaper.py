'''
Created on 30/01/2010

@author: jim
'''
import sys
import os.path

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
    parser.add_option("-i",
                      "--ignore-stored-hashes",
                      dest="ignorehashes",
                      action="store_true",
                      help="ignores stored calculated hashes in .digest " + 
                      "hidden files, this means every hash will be " + 
                      "recalculated")
    parser.add_option("-o",
					  "--output-path",
					  dest="outputpath",
					  action="store",
					  help="Moves detected collisionated files to the given " + 
					  "output path")
    
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
            print "path " + path + " does not exists"
            sys.exit(1)
            
        br.digest(path)
    
    duplicated = br.getCollisions()
    if duplicated:
        print "Duplicateds found"
    
    print "Done"
    sys.exit(0)


if __name__ == '__main__':
    main()

