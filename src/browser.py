'''
Created on 30/01/2010

@author: jim
'''
import io
import os
import sys
import pickle
from os.path import join 

from posixpath import splitext
from pickle import PicklingError, PickleError
from string import lower

from digester import FileDigester

class Walker(object):
    
    _extension = None
    _store_hash = False
    _verbose = False
    _ignore_hashes = False
    
    _hashDictionary = {}
    _collisions = {}

    def __init__(self, extension = None, \
                 store_hash = False, \
                 verbose = False, \
                 ignore_hashes = False):
        '''
        Constructor
        '''
        self._extension = extension
        self._store_hash = store_hash
        self._verbose = verbose
        self._ignore_hashes = ignore_hashes
        
    
    def digest(self, basepath):
        ''' Starts the digestion of files '''
        self._walk(basepath)
        
        
    def getCollisions(self):
        if self._verbose:
            if self._collisions:
                for key in self._collisions.iterkeys():
                    files = self._collisions[key]
                    self._debug( ("The following {0} files share the same hash " + 
                        "{1}").format(len(files), key))
                    for file in files:
                        self._debug("\t" + file)

        return self._collisions
        
    
    def _walk(self, walkpath):
        '''
        Walks througt all the files in the given path and calculates every sha1 and then stores it in
        a file named as the original
        '''
        for d in list(os.walk(walkpath)):
            dirpath = d[0]
            filenames = d[2]
               
            self._debug("Digesting " + dirpath)
            
            for file in filenames:
                if file.startswith("."): # ignore hidden files
                    continue
                
                (name, extension) = splitext(file)
                if self._extension != None and lower(extension[1:]) != lower(self._extension):
                    continue
                
                filepath = join(dirpath, file)
                digestedPath = join(dirpath, '.' + name + '.digest')
                
                if not self._ignore_hashes:
                    digested = self._digested(filepath, digestedPath)
                else:
                    digested = None
                    
                if not digested:
                    predigested = False
                    digested = self._digest(filepath, digestedPath)
                else:
                    predigested = True
                
                if not digested:
                    self._debug('File ' + filepath + ' could not be digested')
                elif not predigested:
                    self._debug('File ' + filepath + ' digested')
                else:
                    self._debug('File ' + filepath + ' already digested, skipping')
                
                if digested:
                    self._putValue(digested)


    def _digest(self, filepath, digestedPath):
        ''' Actually digest the given file and stores the digest result in the given path '''
        digester = FileDigester(filepath)
        digested = digester.digest()
        if digested == None:
            return None
        
        if self._store_hash:
            try:
                digestedFile = io.open(digestedPath, 'bw')
                pickle.dump(digested, digestedFile)
                digestedFile.close()
            except PicklingError as e:
                self._debug(e[0])
            except Exception as e:
                self._debug(e[0])
        
        return digested
        
        
        
    def _digested(self, filepath, digestedPath):
        ''' Checks if the given file is digested in the given digested path, and checks if they declare the same file size '''
        if os.path.isfile(digestedPath) and os.path.getsize(digestedPath) > 0:
            try:
                digestedFile = io.open(digestedPath, 'br')
                digested = pickle.load(digestedFile)
                digestedFile.close()
                digestedSize = digested['size']
                
                size = os.path.getsize(filepath)
                
                if size == digestedSize:
                    return digested
                else:
                    return None
                
            except PickleError as e:
                self._debug(e)
            except Exception as e:
                self._debug(e)
        return None
    
    
    def _putValue(self, digested):
        hash = digested["hash"]
        path = digested["path"]
        
        if self._hashDictionary.has_key(hash):
            self._debug("Collision detected for hash " + hash)
            
            collision = None
            if self._collisions.has_key(hash):
                collision = self._collisions[hash]
            else:
                collision = [self._hashDictionary[hash]]
                
            collision.append(path)
            
            self._collisions[hash] = collision
            
        else:
            self._hashDictionary[hash] = path
        

    
    
    def _out(self, message):
        sys.stdout.write("Walker: " + message + "\n")
    
    
    def _debug(self, message):
        if self._verbose:
            self._out(message)
            

    
