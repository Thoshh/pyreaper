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
                      "--no-action",
                      dest="noaction",
                      action="store_true",
                      help="does not executes any file action")
    parser.add_option("-d",
                      "--delete",
                      dest="delete",
                      action="store_true",
                      help="delete every duplicated file")
    parser.add_option("-m", 
                      "--move-to",
                      dest="moveto",
                      metavar="DIR",
                      help='Moves duplicated files instead of deleting them')
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
    parser.add_option("-t",
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
        exit_with_error('', parser)
    
    br = Walker(options.extension, \
			options.storehash, \
			options.verbose, \
			options.ignorehashes)

    action = None
    moveto = None
    rmcommands = False
    
    if options.noaction:
        action = 'n'
        
    elif options.moveto:
        action = 'm'
        moveto = options.moveto
        
        if not moveto:
            exit_with_error('No "move to" target provided', parser)
            
        elif not os.path.exists(moveto):
            exit_with_error('Path %s does not exists' % moveto, parser)
            
        elif not os.path.isdir(moveto):
            exit_with_error('Path %s is not a directory' % moveto, parser)
        
    elif options.delete:
        action = 'd'
        rmcommands = options.rmcommands
        
        
    if action is None:
        exit_with_error('No action selected', parser)

    for path in args:
        if not os.path.exists(path):
            exit_with_error("path {0} does not exists".format(path), parser)
        br.digest(path)
    
    duplicates = br.collisions()
    clean = False
    
    if duplicates:

        print "Duplicates found, cleaning..."
        c = Cleaner(
                    duplicates,
                    options.interactive,
                    options.verbose,
                    action,
                    rmcommands,
                    options.noconfirmation,
                    moveto)

        clean = c.clean()
        
    else:
        print "No duplicates found"
        
    if not options.storehash:
        print "Deleting digest files..."
        c = Cleaner(verbose = options.verbose)
        c.delete(br.digestFiles(), -1, True)
        
        
    if options.deletedirs:
        c = Cleaner(verbose = options.verbose)
        for path in args:
            empty_dirs = br.findEmptyDirs(path)
            for dir in empty_dirs:
                if options.rmcommands or options.dontdelete:
                    print "Keeping empty tree {0}".format(dir)
                else:
                    c.deleteDir(dir)
        
    if clean:
        sys.exit(0)
    else:
        sys.exit(1)


def exit_with_error(message, parser):
    if message:
        print message
    parser.print_help()
    sys.exit(1)
    

if __name__ == '__main__':
    main()

