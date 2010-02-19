'''
@author: Pablo Carranza
'''

from distutils.core import setup

setup(name='Reaper', 
      version='0.0.1',
      description='File reaper, detects duplicated files and deletes them',
      author='Pablo Carranza',
      author_email='pcarranza@gmail.com',
      packages=['pyreaper'],
      package_dir={'pyreaper': 'src/pyreaper'},
      scripts=['src/reaper'])