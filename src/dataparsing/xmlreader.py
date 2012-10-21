'''
Created on Aug 13, 2012

@author: Alex
'''
import xml.etree.cElementTree as et
import cPickle as pkl
import csv

class XmlMatrix(object):
    '''
    classdocs
    '''
    def __init__(self, filename):
        '''
        Constructor
        '''
        self.tree = et.ElementTree(file=filename)
        self.matrix = None
        
    def getMatrix(self):
        if self.matrix is not None:
            return self.matrix
        self.matrix = {}
        for taxon in self.tree.iter(tag='TaxonEntry'):
            taxonId = taxon.attrib.values()[0]
            #each taxon id maps to a list of {items_attributes:[item list]} dicts
            if not self.matrix.has_key(taxonId):
                self.matrix[taxonId] = []
            for items in taxon:
                name = items.attrib['name']
#                dbname = items.attrib['databaseName']
#                itemType = items.attrib['itemType']
                # we keep a list of states in case of polymorphism
                states = []
                for item in items:
#                    item_attr = item.attrib
                    item_value = item.text
                    # need to do this to get rid of excessive whitespace in between words (particularly species name)
                    item_value = ' '.join(item_value.split()).strip()
                    if item_value == 'Yes':
                        states.append(True)
                    elif item_value == 'No':
                        states.append(False)
                    else:
                        states.append(item_value)
                self.matrix[taxonId].append({name:states})
        return self.matrix
    
class CsvMatrix(object):

    def __init__(self, filename, delim='\t'):
        self.reader = csv.DictReader(open(filename), delimiter=delim)
        self.matrix = None
        
    def getMatrix(self):
        if self.matrix is not None:
            return self.matrix
        self.matrix = {}
        tid = 0
        for row in self.reader:
            self.matrix[tid] = []
            for key in row:
                if row[key].find('|') != -1:
                    states = [row[key].split('|')[0]]
                else:
                    states = [row[key]]
                self.matrix[tid].append({key : states})
            tid += 1
        return self.matrix
        
        
if __name__ == "__main__":
    c = CsvMatrix('../../data/achillea.txt')
    matrix = c.getMatrix()
    for k, v in matrix.iteritems():
        print k, v
    