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

import os

class Cleaner(object):
    
    __duplicates = None
    __interactive = True
    __verbose = False
    __rmcommands = False
    __noconfirmation = False
    __action = 'd'
    _moveto = None
    
    def __init__(self, \
                 duplicates = None,
                 interactive = True,
                 verbose=False,
                 action = 'n',
                 rmcommands = False,
                 noconfirmation = False,
                 moveto = None ):
        self.__duplicates = duplicates
        self.__verbose = verbose
        self.__interactive = interactive
        self.__rmcommands = rmcommands
        self.__noconfirmation = noconfirmation
        self.__action = action
        self._moveto = moveto
    
    
    def clean(self):
        
        action_command = 'no_action'
        
        if self.__action == 'd':
            if self.__rmcommands:
                action_command = 'print_delete'
            else:
                action_command = 'delete'

            if not self.__interactive and not self.__noconfirmation:
                sure = raw_input("WARNING: this will delete all duplicates " + 
                                 "found but the first one, are you sure? Y/[N] ")
                if not sure or not (sure.lower() == "y" or sure.lower() == "yes"):
                    print "Quiting"
                    return False
                
            elif self.__noconfirmation:
                print "Skipping confirmation..."
                
        elif self.__action == 'm':
            action_command = 'move'
            
            if self._moveto is None:
                print 'Requested action is "move" but no destination path was provided'
            
            if not os.path.exists(self._moveto):
                print 'Requested action is "move" but no destination path was provided'
            
        elif self.__verbose:
            print "Not deleting anything, no confirmation required"
        
        
        if self.__rmcommands:
            print "# Printing cleanup script..."
            print "# -------------- SCRIPT START --------------"
            
        
        for key in self.__duplicates.iterkeys():
            files = self.__duplicates[key]
            
            if self.__interactive:
                self.ask(files, action_command)
            else:
                self.keep_first(files, action_command)
                
        if self.__rmcommands:
            print "# -------------- SCRIPT END --------------"
    
        return True
        
    
    def ask(self, files, action):
        funct = getattr(self, action)
        
        print ""
        maxfile = 1
        for file in files:
            print "{0} - {1}".format(maxfile, file)
            maxfile += 1
        
        
        print "[leave empty to ignore these files]"
        pick = raw_input("pick which file survives: ")
        if not pick: # Ignoring
            return False
        
        elif str(pick).isdigit():
            index = int(pick)
            self._debug("processing index {0} of {1}".format(index, maxfile - 1))
            
            if index >= maxfile:
                print "Option not valid (out of range), skipping"
                return False
            
            else:
                funct(files, index)
                return True
                
        else:
            print "Wrong input, skipping"
            return False
    
    
    def keep_first(self, files, action):
        funct = getattr(self, action)
        funct(files, 1)
    
    
    
    def delete(self, files, keep, quiet = False):
        index = 1
        
        for file in files:
            if index == keep:
                self._debug("keeping {0}".format(file))
            else:
                try:
                    if not quiet:
                        print "deleting {0}".format(file)
                    os.remove(file)
                except:
                    print "Could not delete {0}".format(file)
            index += 1
    
    def print_delete(self, files, keep, quiet=False):
        index = 1
        
        for file in files:
            if index == keep:
                print " # keeping '{0}'".format(file)
            else:
                print "rm '{0}'".format(file)
            index += 1
    
    
    def move(self, files, keep, quiet=False):
        index = 1
        
        if str(self._moveto).endswith('/'):
            new_path = os.path.dirname(self._moveto)
        else:
            new_path = self._moveto
        
        for file in files:
            if index != keep:
                new_file = new_path + str(file)
                new_file_path = os.path.dirname(new_file)
                if not os.path.exists(new_file_path):
                    os.makedirs(new_file_path)
                    
                os.rename(file, new_file)
            index += 1
    
    
    def no_action(self, files, keep, quiet=False):
        index = 1
        
        for file in files:
            if index != keep:
                print "File '{0}' would have been deleted".format(file)
            index += 1
    
    
            
    def deleteDir(self, path):
        try:
            print "Removing empty tree {0}".format(path)
	    for digestfile in os.listdir(path):
		file = os.path.join(path, digestfile)
		os.remove(file)

            os.removedirs(path)
        except:
            print "Could not remove {0}".format(path)
            

    def _debug(self, message):
        if self.__verbose:
            print message

    def build_path(self, files, keep):
        pass
