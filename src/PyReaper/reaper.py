'''
PyReaper is a small tool to find and delete duplicated files 
Copyright (C) 2010  Pablo Carranza

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

@author: Pablo Carranza <pcarranza@gmail.com>
'''
import sys
import os.path

from cleaner import Cleaner
from optparse import OptionParser
from browser import Walker


def main():
    parser = OptionParser(prog="reaper",
                          version="0.1.0",
                          usage="%prog [options] <path to folder> "+
                          "[<path to folder...>]",
                          description="PyReaper is a small tool that detects " + 
                          "duplicated files by hashing them and then deletes " + 
                          "these duplicated files leaving just one of them", 
                          epilog="CAUTION: handle with EXTREME CARE, " + 
                          "use -n option first if you are not sure of " + 
                          "what are you doing, this thing deletes stuff!!!")
    parser.add_option("-n",
                      "--dont-delete",
                      dest="dontdelete",
                      action="store_true",
                      help="skips delete process, useful for only " + 
                      "detect duplicates or create the digests")
    parser.add_option("-p",
                      "--print-rm-commands",
                      dest="rmcommands",
                      action="store_true",
                      help="skips delete process and prints a set of \"rm\" " + 
                      "commands so you can delete the duplicate files yourself")
    parser.add_option("-i",
                      "--interactive",
                      dest="interactive",
                      action="store_true",
                      help="interactive mode, will ask for each duplicate. " + 
                      "By default it deletes every duplicate found but " + 
                      "the first one")
    parser.add_option("-y",
                      "--dont-ask-confirmation",
                      dest="noconfirmation",
                      action="store_true",
                      help="skips confirmation question. ")
    parser.add_option("-s",
                      "--store-hashes",
                      dest="storehash",
                      action="store_true",
                      help="store and keep calculated hashes in .digest hidden files ")
    parser.add_option("-d",
                      "--delete-empty-trees",
                      dest="deletedirs",
                      action="store_true",
                      help="deletes empty trees when finishes")
    parser.add_option("-e", 
                      "--ext", 
                      dest="extension", 
                      action="store",
                      help="only digests files with the given extension" )
    parser.add_option("-v",
                      "--verbose",
                      dest="verbose",
                      action="store_true",
                      help="outputs much more information during process " + 
                      "(sometimes even too much)")
    parser.add_option("",
                      "--ignore-stored-hashes",
                      dest="ignorehashes",
                      action="store_true",
                      help="ignores stored calculated hashes in .digest " + 
                      "hidden files, this means every hash will be " + 
                      "recalculated")
    
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
    
    if duplicates:
        print "Duplicates found, cleaning..."
        c = Cleaner(duplicates, \
                options.interactive, \
                options.verbose,
                options.dontdelete,
                options.rmcommands,
                options.noconfirmation)
        clean = c.clean()
        
    else:
        print "No duplicates found"
        
    if not options.storehash:
        print "Deleting digest files..."
        c = Cleaner(verbose = options.verbose)
        c.delete(br.digestFiles(), -1, True)
        
        
    if options.deletedirs and not (options.rmcommands or
                                   options.dontdelete):
        c = Cleaner(verbose = options.verbose)
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

