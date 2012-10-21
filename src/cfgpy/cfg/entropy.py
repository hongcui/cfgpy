'''
Created on Aug 20, 2012

@author: Alex Dusenbery (adusen@cs.umb.edu)
(Ported from javascript implementation written by Swami Iyer (swamir@cs.umb.edu))

Implements the information gain algorithm from the stanford paper titled:
"Optimization for the EcoPod field identification tool"
'''
import math

class Entropy(object):
    
    def __init__(self, matrix, uniform=True, speciesCount={}, entropy_fn=None, sp_weight_fn=None, char_cost_fn=None):
        '''
        @param matrix Maps species names to dictionary of char:val
        @param uniform True if we don't consider species abundance in calculations, false otherwise
        @param speciesCount Dictionary mapping species names to counts/abundance.
        '''
        self.uniform = uniform
        self.matrix = matrix
        self.speciesCount = speciesCount
        self.entropy_function = entropy_fn
        self.species_weighting_function = sp_weight_fn
        self.character_cost_function = char_cost_fn

    def character_entropy(self, sp_list, char):
        '''
        Calculates the entropy of a character, either uniformly or depending on
        distribution of value (boolean) for the character.
        @param sp_list A list of species that have the given character-state
        @param char The character in question (required for reporting purposes only).
        '''
        if self.uniform:
            try:
                p = 1.0 / len(sp_list)
                return -len(sp_list) * p * math.log(p, 2)
            except ZeroDivisionError:
                print 'No species have the character', char
                return 0.0
        else:
            total = float(sum([self.speciesCount(sp) for sp in sp_list]))
            h = 0
            for sp in sp_list:
                p = self.speciesCount[sp] / total
                h += p * math.log(p, 2)
            return -h
    
    def species_entropy(self):
        '''
        Calculates the species entropy, either depending on species distribution or not.
        '''
        if self.uniform:
            p = 1.0 / len(self.matrix)    #if considering uniform dist., each species is equally likely to appear.
            return -len(self.matrix) * (p * math.log(p, 2))
        else:
            total = float(sum(self.speciesCount.values()))   #total num of occurrences
            h = 0
            for sp in self.speciesCount:
                p = self.speciesCount[sp] / total    #gets relative frequency of occurrences of this species
                h += p * math.log(p, 2)
            return -h
        
    def conditional_entropy(self, c):
        '''
        Returns the conditional entropy of character c.
        '''
        states = {}
        for sp in self.matrix:
            try:
                state = str(self.matrix[sp][c])
                if state in states:
                    states[state].append(sp)
                else:
                    states[state] = [sp]
            except KeyError:
                print 'No character for this species:', c, sp
        s_keys = states.keys()
        p_states = [float(len(states[s])) / float(len(self.matrix)) for s in s_keys]
        
#        if p_true == 0:
#            h2 = self.character_entropy(false, c)
#            return p_false * h2
#        elif p_false == 0:
#            h1 = self.character_entropy(true, c)
#            return p_true * h1
        
        return_sum = 0
        for i in xrange(len(s_keys)):
            h = self.character_entropy(states[s_keys[i]], c)
            p = p_states[i]
            return_sum += p * h
        return return_sum
        
    
    def information_gain(self):
        '''
        Calculates the info. gain for each character and returns
        a reverse-sorted dictionary mapping characters each character
        to it's corresponding info. gain value.
        '''
        self.eliminate_redundant_characters()
        hS = self.species_entropy()
        igs = {}
        chars = set([])
        for d in self.matrix.values():
            for ch in d:
                chars.add(ch)
        for ch in chars:
            hC = self.conditional_entropy(ch)
            ig = hS - hC
            igs[ch] = ig
        pairs = igs.items()
        igs = sorted(pairs, reverse=True, key=lambda x: x[1])    #list of reverse-sorted tuples (sorted by ig of each character)    
        return igs
        
    def eliminate_redundant_characters(self):
        '''
        Eliminates characters from the matrix that attain the same value across
        each species in the matrix.
        '''
        chars_to_vals = {}
        for d in self.matrix.values():   #for each species char->val dict
            for ch, val in d.iteritems():     #look at the character and corresponding value
                if ch not in chars_to_vals:
                    chars_to_vals[ch] = set([val])    #store observed values in a set
                else:
                    chars_to_vals[ch].add(val)
        #redundant characters have a cardinality of 1
        redundant = [ch for ch in chars_to_vals if len(chars_to_vals[ch]) == 1]
        #now go through and remove these from our matrix
        for d in self.matrix.values():
            to_remove = [] #store list of chars to remove from this list
            for ch, val in d.iteritems():
                if ch in redundant:
                    to_remove.append(ch)
            for r in to_remove:
                d.pop(r)
        #return the list of characters we've removed
        return redundant
    
    def split_on_character(self, char):
        '''
        Splits the matrix into two submatrices: those that attain value True
        for the given character, and those that attain False.
        '''
        submatrices = {}
        for sp, d in self.matrix.iteritems():
            state = str(d[char])
            if state in submatrices:
                submatrices[state][sp] = d
            else:
                submatrices[state] = {sp : d} 
        return submatrices
                    
    