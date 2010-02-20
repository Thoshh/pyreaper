'''
@author: Pablo Carranza <pcarranza@gmail.com>
'''

from distutils.core import setup

setup(name='Reaper', 
      version='0.0.1',
      description='File reaper, detects duplicated files and deletes them',
      author='Pablo Carranza',
      author_email='pcarranza@gmail.com',
      packages=['PyReaper'],
      package_dir={'PyReaper': 'src/PyReaper'},
      scripts=['src/reaper'])