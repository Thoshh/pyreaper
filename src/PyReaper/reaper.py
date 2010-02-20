'''
@author: Pablo Carranza <pcarranza@gmail.com>
'''
import sys
import os.path

from cleaner import Cleaner
from optparse import OptionParser
from browser import Walker


def main():
    parser = OptionParser(usage="%prog [options] <path to folder> "+
                          "<path to folder...>",
                          description="Small util that detects duplicated " + 
                          "files by hashing files and then deletes these " + 
                          "duplicated files leaving just one of them", 
                          epilog="Handle with extreme care, use -n option " + 
                          "first if you are not sure of what are you doing")
    parser.add_option("-i",
                      "--interactive",
                      dest="interactive",
                      action="store_true",
                      help="Interactive mode, will ask for each duplicate. " + 
                      "By default it deletes every duplicate found but " + 
                      "the first one")
    parser.add_option("-s",
                      "--store-hashes",
                      dest="storehash",
                      action="store_true",
                      help="Store calculated hashes in .digest hidden files " + 
                      "(will delete at the end of the process unless -k " + 
                      "option is indicated)")
    parser.add_option("-k",
                      "--keep-digested",
                      dest="dontclean",
                      action="store_true",
                      help="Keeps .digest files when finishes")
    parser.add_option("-d",
                      "--delete-empty-dirs",
                      dest="deletedirs",
                      action="store_true",
                      help="Deletes empty dirs when finishes")
    parser.add_option("-e", 
                      "--ext", 
                      dest="extension", 
                      action="store",
                      help="Only digests files with the given extension" )
    parser.add_option("-v",
                      "--verbose",
                      dest="verbose",
                      action="store_true",
                      help="Outputs much more information during process " + 
                      "(sometimes even too much)")
    parser.add_option("",
                      "--ignore-stored-hashes",
                      dest="ignorehashes",
                      action="store_true",
                      help="Ignores stored calculated hashes in .digest " + 
                      "hidden files, this means every hash will be " + 
                      "recalculated")
    parser.add_option("-n",
                      "--dont-delete",
                      dest="dontdelete",
                      action="store_true",
                      help="Skips duplicates delete process, " + 
                      "useful to just detect duplicates or create the digests")
    
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
    
    duplicates = br.collisions()
    clean = False
    c = Cleaner(duplicates, \
                options.interactive, \
                options.verbose,
                options.dontdelete)
    
    if duplicates:
        print "Duplicates found, cleaning..."
        clean = c.clean()
        
    else:
        print "No duplicates found"
        
    if not options.dontclean:
        if options.storehash:
            print "Deleting digest files..."
        c.delete(br.digestFiles(), -1, True)
        
        
    if options.deletedirs:
        for path in args:
            empty_dirs = br.findEmptyDirs(path)
            for dir in empty_dirs:
                c.deleteDir(dir)
        
    if clean:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()

