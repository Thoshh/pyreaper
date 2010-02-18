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
        
        for key in self._duplicates.iterkeys():
            files = self._duplicates[key]
            
            if self._interactive:
                self.ask(files)
            else:
                self.keep_first(files)
    
        return True
        
    
    def ask(self, files):
        
        index = 1
        for file in files:
            print "{0} - {1}".format(index, file)
            index += 1
        
        print "[leave empty to ignore these files]"
        pick = raw_input("pick which file survives: ")
        if not pick: # Ignoring
            return False
        
        elif str(pick).isdigit():
            
            if int(pick) > index:
                print "Option not valid (out of range), skipping"
                return False
            
            else:
                self.delete(files, int(pick))
                return True
                
        else:
            print "Wrong input, skipping"
            return False
    
    
    def keep_first(self, files):
        delete(files, 1)
    
    
    def delete(self, files, which):
        for index in range(len(files)):
            if index == which - 1:
                self.debug("keeping {0}".format(files[index]))
            else:
                self.debug("deleting {0}".format(files[index]))
                try:
                    os.remove(files[index])
                except:
                    print "Could not delete {0}".format(files[index])
        
        pass

    def debug(self, message):
        if self._verbose:
            print message

