'''
@author: pcarranza@gmail.com
'''

import os

class Cleaner(object):
    
    _duplicates = None
    _interactive = True
    _verbose = False
    _dontdelete = False
    
    def __init__(self, \
                 duplicates, \
                 interactive = True, \
                 verbose=False,
                 dontdelete = False ):
        self._duplicates = duplicates
        self._verbose = verbose
        self._interactive = interactive
        self._dontdelete = dontdelete
    
    
    def clean(self):
        
        if not self._dontdelete:
            if not self._interactive:
                sure = raw_input("WARNING: this will delete all duplicates " + 
                                 "found but the first one, are you sure? Y/[N] ")
                if not sure or not (sure.lower() == "y" or sure.lower() == "yes"):
                    print "Quiting"
                    return False
        else:
            print "Not deleting anything, no confirmation required"
        
        for key in self._duplicates.iterkeys():
            files = self._duplicates[key]
            
            if not self._dontdelete and self._interactive:
                self.ask(files)
            else:
                self.keep_first(files)
    
        return True
        
    
    def ask(self, files):
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
            self._debug("deleting index {0} of {1}".format(index, maxfile - 1))
            
            if index >= maxfile:
                print "Option not valid (out of range), skipping"
                return False
            
            else:
                self.delete(files, index - 1)
                return True
                
        else:
            print "Wrong input, skipping"
            return False
    
    
    def keep_first(self, files):
        self.delete(files, 1)
    
    
    def delete(self, files, keep, quiet = False):
        index = 1
        for file in files:
            if index == keep:
                self._debug("keeping {0}".format(file))
            else:
                try:
                    if self._dontdelete:
                        print "File {0} would have been deleted".format(file)
                    else:
                        if not quiet:
                            print "deleting {0}".format(file)
                        os.remove(file)
                        
                except:
                    print "Could not delete {0}".format(file)
            index += 1
            
            
    def deleteDir(self, path):
        try:
            if self._dontdelete:
                print "Empty tree {0} would have been deleted".format(path)
            else:
                print "Removing empty tree {0}".format(path)
                os.removedirs(path)
        except:
            print "Could not remove {0}".format(path)
            

    def _debug(self, message):
        if self._verbose:
            print message

    