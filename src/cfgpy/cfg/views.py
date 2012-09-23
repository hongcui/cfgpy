from models import DatasetXml
from django import forms
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from cfgpy.cfg.forms import SpeciesSelect, ComputeForm, SplitForm
from cfgpy.cfg import entropy

DEBUG_MODE = False  # turn this on to see information gain values in character lists, and redundant characters

def species(request, dataset_id):
    if request.method == 'POST': #if the form has been submitted
        form = SpeciesSelect(request.POST)
        if form.is_valid():
            selected =  request.POST.getlist('species')
            dataset = get_object_or_404(DatasetXml, pk=dataset_id)
            matrix = dataset.get_species_keyed_dictionary(includedSpecies=selected)
            e = entropy.Entropy(matrix)
            compute_redundant_and_ig(request, e, 'redundant', 'ig')
            return HttpResponseRedirect('compute/')
        else:
            print 'not valid'
    else:
        dataset = get_object_or_404(DatasetXml, pk=dataset_id)
        choices = dataset.get_species_names()
        choices = [(c, c) for c in choices]  
        form = SpeciesSelect()          
        form.fields['species'] = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'size':15}), 
                                                           required=True,
                                                           choices=choices)
        
    return render(request, 'cfg/species.html', {'form':form})

def compute(request, dataset_id):
    if request.method == 'POST':
        form = ComputeForm(request.POST)
        if form.is_valid():
            selected_char = request.POST.getlist('characters')[0]
            request.session['split_char'] = selected_char
            e = request.session['entropy']  # get the current Entropy object
            true, false = e.split_on_character(selected_char)
            request.session['true_matrix'] = true
            request.session['false_matrix'] = false
            return HttpResponseRedirect('split/')
        else:
            print 'Not valid in compute form.'
    else:
        last_ig = request.session['ig'][-1]
        redundant = request.session['redundant'][-1]
        matrix = request.session['entropy'].matrix
        if DEBUG_MODE:
            choices = [(i[0], i) for i in last_ig]
        else:
            choices = [(i[0], i[0]) for i in last_ig]
        form = ComputeForm()
        form.species = sorted(matrix.keys())
        form.redundant = redundant
        form.debug = DEBUG_MODE
        form.fields['characters'] = forms.ChoiceField(widget=forms.RadioSelect,
                                                              required=False,
                                                              choices=choices)
    return render(request, 'cfg/compute.html', {'form':form})

def split_species(request, dataset_id):
    if request.method == 'POST':
            form = SplitForm(request.POST)
            if form.is_valid():
                select_true_false = request.POST.getlist('select_true_false')
                if select_true_false[0].lower() == 'true':
                    matrix = request.session['true_matrix']
                else:
                    matrix = request.session['false_matrix']
                # reset entropy using the true/false matrix (i.e. split the decision tree)
                ent = entropy.Entropy(matrix)
                request.session['entropy'] = ent
                compute_redundant_and_ig(request, ent, 'redundant', 'ig')
                return HttpResponseRedirect('/cfg/'+dataset_id+'/compute/')
            else:
                print 'Not valid in compute form.'
    else:
        form = SplitForm()
        true = request.session['true_matrix']
        false = request.session['false_matrix']
        form.true_species = sorted(true.keys())
        form.false_species = sorted(false.keys())
        form.split_char = request.session['split_char']
        choices = (('true', 'true'), ('false', 'false'))
        form.fields['select_true_false'] = forms.ChoiceField(widget=forms.RadioSelect,
                                                       required=True,
                                                       choices=choices)
        
    return render(request, 'cfg/split.html', {'form':form})

def compute_redundant_and_ig(request, ent, red_key, ig_key):
    '''
    Helper method for the above functions.  Given an entropy object, this
    eliminates the redundant characters for it's matrix, then stores the list
    of redundant chars and IG list in the request's session.
    @param request HTTP request object (of which we store results in session)
    @param ent The entropy object to use.
    @param red_key The key to store redundant list in for the session
    @param ig_key The key to store the IG list in for the session.
    '''
    redundant = ent.eliminate_redundant_characters()
    try:
        request.session[red_key].append(redundant)
    except KeyError:
        request.session[red_key] = [redundant]
    ig = ent.information_gain()
    # store this in the session 'ig' list (or make a new list with ig as first element).
    try:
        request.session[ig_key].append(ig)
    except KeyError:
        request.session[ig_key] = [ig]
    request.session['entropy'] = ent