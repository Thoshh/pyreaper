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
    
    _digestFiles = []

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
        
        
    def collisions(self):
        if self._verbose:
            if self._collisions:
                for key in self._collisions.iterkeys():
                    files = self._collisions[key]
                    self._debug( ("The following {0} files share the same hash " + 
                        "{1}").format(len(files), key))
                    for file in files:
                        self._debug("\t" + file)

        return self._collisions
    
    
    def digestFiles(self):
        return self._digestFiles
        
        
    def findEmptyDirs(self, path):
        emptydirs = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            if not filenames and not dirnames:
                emptydirs.append(dirpath)
        return emptydirs
        
    
    def _walk(self, walkpath):
        '''
        Walks througt all the files in the given path and calculates every sha1 and then stores it in
        a file named as the original
        '''
        for d in list(os.walk(walkpath)):
            dirpath = d[0]
            filenames = d[2]
               
            self._out("Digesting {0}".format(dirpath))
            
            for file in filenames:
                if file.startswith("."): # ignore hidden files
                    continue
                
                (name, extension) = splitext(file)
                if self._extension != None and lower(extension[1:]) != lower(self._extension):
                    continue
                
                filepath = join(dirpath, file)
                digestedPath = join(dirpath, '.{0}.digest'.format(name))
                
                if not self._ignore_hashes:
                    try:
                        digested = self._digested(filepath, digestedPath)
                    except:
                        digested = None
                else:
                    digested = None
                    
                if not digested:
                    predigested = False
                    digested = self._digest(filepath, digestedPath)
                else:
                    predigested = True
                
                if not digested:
                    self._out('File {0} could not be digested'.format(filepath))
                elif not predigested:
                    self._debug('File {0} digested'.format(filepath))
                else:
                    self._debug('File {0} already digested, skipping'.format(filepath))
                
                if digested:
                    self._putValue(digested)
                    
                    if os.path.isfile(digestedPath):
                        self._digestFiles.append(digestedPath)


    def _digest(self, filepath, digestedPath):
        ''' Actually digest the given file and stores the digest result in the given path '''
        digester = FileDigester(filepath)
        try:
            digested = digester.digest()
        except IOError:
            self._out("Cannot open file {0} for reading, skipping".format(filepath))
            return None
        
        if digested == None:
            return None
        
        if self._store_hash:
            try:
                self._debug("Saving digest status to file {0}".format(digestedPath))
                digestedFile = io.open(digestedPath, 'bw')
                pickle.dump(digested, digestedFile)
                digestedFile.close()
            except PicklingError as e:
                self._out(str(e[1]))
            except IOError as e:
                self._out("Cannot open file {0} for writing".format(digestedPath))
            except Exception as e:
                self._debug(e.__class__ + " - " + str(e[1]))
        
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
        if not 'hash' in digested or not 'path' in digested:
            self._out('Could not use this predigested file, remove it and relaunch process')
            return
        
        hash = digested['hash']
        path = digested['path']
        
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
        sys.stdout.write(message + "\n")
    
    
    def _debug(self, message):
        if self._verbose:
            self._out(message)
            

    
