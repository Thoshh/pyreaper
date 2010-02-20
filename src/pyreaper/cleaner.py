'''
@author: pcarranza@gmail.com
'''

import os

class Cleaner(object):
    
    _duplicates = None
    _interactive = True
    _verbose = False
    
    def __init__(self, \
                 duplicates, \
                 interactive = True, \
                 verbose=False ):
        self._duplicates = duplicates
        self._verbose = verbose
        self._interactive = interactive
    
    
    def clean(self):
        
        if not self._interactive:
            sure = raw_input("WARNING this will delete all duplicates found " + \
                    "but the first one found, are you sure? Y/[N] ")
            if not sure or not (sure.lower() == "y" or sure.lower() == "yes"):
                print "Quiting"
                return False
        
        for key in self._duplicates.iterkeys():
            files = self._duplicates[key]
            
            if self._interactive:
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
            self.debug("deleting index {0} of {1}".format(index, maxfile - 1))
            
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
    
    
    def delete(self, files, keep):
        index = 1
        for file in files:
            if index == keep:
                self.debug("keeping {0}".format(files[index]))
            else:
                print "deleting {0}".format(files[index])
                try:
                    os.remove(files[index])
                except:
                    print "Could not delete {0}".format(files[index])
            index += 1
            

    def debug(self, message):
        if self._verbose:
            print message

