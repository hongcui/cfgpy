'''
Created on Aug 24, 2012

@author: Alex
'''
import unittest
import entropy
from cfgpy.cfg.models import DatasetXml

class Test(unittest.TestCase):

    dataset = None

    def setUp(self):
        self.dataset = DatasetXml.objects.all()[0]  

    def tearDown(self):
        self.dataset = None

    def testRedundant(self):
        included = ['Erynnis juvenalis', 'Pompeius verna']
        matrix = self.dataset.get_species_keyed_dictionary(included)
        e = entropy.Entropy(matrix)
        print e.eliminate_redundant_characters()
        for v in e.matrix.values():
            print v
            
    def testInfoGain(self):
        matrix = self.dataset.get_species_keyed_dictionary()
        e = entropy.Entropy(matrix)
        ig = e.information_gain()
        for pair in ig:
            print pair


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()