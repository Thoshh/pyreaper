'''
Created on 30/01/2010

@author: jim
'''
import os
import pickle
import io

from digester import FileDigester
from os.path import join 
from posixpath import splitext
from pickle import PicklingError, PickleError

class MyBrowser(object):


    def __init__(self):
        '''
        Constructor
        '''

    
    def digest(self, basepath):
        ''' Starts the digestion of files '''
        self.__walk__(basepath)
    
    
        
    
    def __walk__(self, walkpath):
        '''
        Walks througt all the files in the given path and calculates every sha1 and then stores it in
        a file named as the original
        '''
        for dirpath, dirnames, filenames in os.walk(walkpath):
            print "checking " + dirpath
            for dir in dirnames:
                self.__walk__(join(dirpath, dir))
                
            for file in filenames:
                if file.startswith("."):
                    continue
                
                filepath = join(dirpath, file)
                digestedPath = join(dirpath, '.' + splitext(file)[0] + '.digest')
                
                if self.__digested__(filepath, digestedPath):
                    continue
                
                if self.__digest__(filepath, digestedPath):
                    print 'File ' + filepath + ' digested'
                else:
                    print 'File ' + filepath + ' could not be digested'
                    

                    
    def __digest__(self, filepath, digestedPath):
        ''' Actually digest the given file and stores the digest result in the given path '''
        digester = FileDigester(filepath)
        digested = digester.digest()
        if digested == None:
            return False
        
        try:
            digestedFile = io.open(digestedPath, 'bw')
            pickle.dump(digested, digestedFile)
            digestedFile.close()
        except PicklingError as e:
            print e[0]
        except Exception as e:
            print e[0]
        
        return True
            
        
        
    def __digested__(self, filepath, digestedPath):
        ''' Checks if the given file is digested in the given digested path, and checks if they declare the same file size '''
        if os.path.isfile(digestedPath) and os.path.getsize(digestedPath) > 0:
            try:
                digestedFile = io.open(digestedPath, 'br')
                digested = pickle.load(digestedFile)
                digestedFile.close()
                digestedSize = digested['size']
                
                size = os.path.getsize(filepath)
                
                if size == digestedSize:
                    print 'File ' + filepath + ' already digested'
                    return True
                
            except PickleError as e:
                print e
            except Exception as e:
                print e
        return False
                
                
                
    
    
    
    