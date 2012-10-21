'''
Created on Oct 19, 2012

@author: Alex
'''
import datetime
import sys
from django.core import management
import cfgpy.settings as settings
management.setup_environ(settings)
from cfgpy.cfg.models import DatasetXml
from dataparsing.xmlreader import XmlMatrix, CsvMatrix
xmlmatrix = CsvMatrix('c:/workspace/cfgpy/data/achillea.txt')
import hashlib #for creating a unique dataset id
h = hashlib.md5()
matrix = xmlmatrix.getMatrix()
h.update(str(matrix))
dataset_id = h.hexdigest() #we can use this as a unique id for the dataset in the database.
d = DatasetXml(dataset_id=dataset_id, name='test-csv-dataset-5', date_created=datetime.datetime.now(), created_by='alex', matrix=matrix)
sys.path.append('c:/workspace/cfgpy/src/cfgpy')
print d
d.save() #this saves the dataset object to the database