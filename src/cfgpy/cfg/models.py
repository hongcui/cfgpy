from django.db import models
import cPickle as pkl
from picklefield.fields import PickledObjectField
from dataparsing.xmlreader import XmlMatrix

class DatasetXml(models.Model):
    '''
    This needs to be created from an interactive python shell with Django
    environment imported.
    @param dataset_id Primary key for this dataset (in the backend table as well as globally, we hope).
    Preferred method for generating this is with python's hashlib, calling update() on the matrix dictionary when
    viewed as a string.  
    @param name A simple name to call this database
    @param date_created The date the dataset was created/added to this database.
    @param matrix A matrix object stored as a python dict object (keyed by species string and valued by dicts
    that map character strings to states).  This gets serialized "on the way in", i.e. there is no 
    need to serialize your object before storing it.
    Example:
    ################
    import hashlib
    from cfgpy.cfg.models import DatasetXml
    h = hashlib.md5()
    matrix = #some dictionary object
    h.update(str(matrix))
    dataset_id = h.hexdigest()
    # Specifying parameter names matters here!
    d = DatasetXml(dataset_id=dataset_id, name='my-dataset', date_created=datetime.datetime.now(), created_by='alex', matrix=matrix)
    d.save()    #Save the object into the database.
    ################
    '''
    dataset_id = models.CharField(primary_key=True, max_length=200)
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField('date created')
    created_by = models.CharField(max_length=200)
    matrix = PickledObjectField() #this needs to be a dictionary returned by XmlReader.getMatrix()
    
    def __unicode__(self):
        return ', '.join([str(self.dataset_id), str(self.name), str(self.date_created), str(self.created_by)])
    
    def get_species_names(self):
        if self.matrix is None:
            print 'Must first call getMatrix() on XmlMatrix object.'
            return None
        species_names = []
        for tid, charStateList in self.matrix.iteritems():
            for charState in charStateList:
                if 'species' in charState:
                    species_names.append(charState['species'][0])
                    #only one of these, so stop looking in the current list
                    break
                elif 'Name' in charState:
                    species_names.append(charState['Name'][0])
                    break
        return species_names
    
    def get_species_keyed_dictionary(self, includedSpecies=None):
        '''
        Returns a dictionary keyed by species name and valued by dict
        mapping chars to values.
        @param A list of species to include (or None is whole matrix is desired).
        '''
        non_chars = ("family", "subfamily", "species")
        species_dict = {}   #maps species names to char/state dicts
        for tid, charStateList in self.matrix.iteritems():
            sp_name  =''    #The name of the current species
            sp_dict = {}    #dict mapping char name to single state for a single species
            for charState in charStateList:
                if 'species' in charState:
                    sp_name = charState['species'][0]
                elif 'Name' in charState:
                    sp_name = charState['Name'][0]
                else:
                    name = charState.keys()[0]  #get name of this key
                    value = charState[name][0]  #original matrix has list of values, so get out first element
                    if name not in non_chars:
                        sp_dict[name] = value
            if includedSpecies is None or sp_name in includedSpecies:
                species_dict[sp_name] = sp_dict
        return species_dict
        