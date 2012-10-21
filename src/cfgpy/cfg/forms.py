'''
Created on Aug 24, 2012

@author: Alex
'''
from django import forms

class SpeciesSelect(forms.Form):
    #really simple form that's just a CharField, but later overwritten to be a choice field
    #(inside the species method in views)
    species = forms.CharField()
    
class ComputeForm(forms.Form):
    # same idea as above
    characters = forms.CharField(required=False)
    species = []
    redundant = []
    display_chars = None
    debug = False
    
class SplitForm(forms.Form):
    split_char = ''
    char_species = {}
    select_state = forms.CharField(required=False)
    