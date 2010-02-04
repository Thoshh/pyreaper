'''
Created on 30/01/2010

@author: jim
'''
import sys
import os.path
from mybrowser import MyBrowser
from optparse import OptionParser


def main():
    parser = OptionParser(usage="%prog [options] <path to folder>")
    parser.add_option("-e", 
                      "--ext", 
                      dest="extension", 
                      action="store",
                      help="filters files for the given extension" )
    parser.add_option("-r",
                      "--recursive",
                      dest="recursive",
                      action="store_true",
                      help="Recurses subdirectories")
    parser.add_option("-k",
                      "--keep-hash-files",
                      dest="keephash",
                      action="store_true",
                      help="keeps the calculated hashes")
    
    (options, args) = parser.parse_args()
    print "extension: " + options.extension
    if options.recursive:
        print "recursive: True"
        
    print "arguments: " + str(len(args))
    if len(args) != 1:
        parser.print_help()
        sys.exit(1)
    
    path=args[0]
    
    if os.path.exists(path) != True:
        parser.print_help()
        print "path " + path + " does not exists"
        sys.exit(1)
        
    br = MyBrowser()
    br.digest(path)
    print "Done"


if __name__ == '__main__':
    main()

