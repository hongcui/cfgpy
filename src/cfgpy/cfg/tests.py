"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import DatasetXml


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class DatasetXml(TestCase):
    d = DatasetXml.objects.all()[0]
    matrix = d.matrix
    included = ['Erynnis juvenalis', 'Pompeius verna']
    
    def test_matrix(self):
        self.assertEqual(len(self.matrix), 119)
        
    def test_sp_matrix_included(self):
        dic = self.d.get_species_keyed_dictionary(self.included)
        self.assertEqual(len(dic), 2)