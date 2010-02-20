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
import hashlib

class FileDigester(object):
    
    _file = None
    
    def __init__(self, filepath):
        self._file = filepath
    
    def digest(self):
        f = io.open(self._file, mode="br")
        sh = hashlib.sha1()
        size = 0
        while 1:
            line = f.readline(1024)
            if len(line) == 0:
                break  
            size += len(line)
            sh.update(line)
        
        if size == 0:
            return None
        
        return {"hash" : sh.hexdigest(), "size" : size, "path" : self._file}
        