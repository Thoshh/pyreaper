'''
Created on 30/01/2010

@author: jim
'''

import io
import hashlib

class FileDigester(object):
    
    file = None
    
    def __init__(self, filepath):
        self.file = filepath
    
    def digest(self):
        f = io.open(self.file, mode="br")
        sh = hashlib.sha1()
        md = hashlib.md5()
        size = 0
        while 1:
            line = f.readline(1024)
            if len(line) == 0:
                break  
            size += len(line)
            sh.update(line)
            md.update(line)
        
        if size == 0:
            return None
        
        return {"sha1" : sh.hexdigest(), "md5" : md.hexdigest(), "size" : size}
        