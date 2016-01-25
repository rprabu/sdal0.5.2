# -*- coding: utf-8 -*-
"""
Created on Sat May 16 09:05:38 2015

@author: prabu
"""

from __future__ import print_function
import re
from collections import defaultdict


class SpectrumRegex:
    #------------------------------------------------------------------------    
    def __init__(self):
        pass
    
    #------------------------------------------------------------------------    
    def make_groups(self, spectrums, suffix):
        #replace X with alphanumeric characters
        alphanum = re.sub(r'X', r'[A-Za-z0-9]+', suffix[1:].upper())        
        #the prefix
        prefix = r'^([\S]*)'
        #the pattern for grouped matching
        patt = r'{}({})$'.format(prefix, alphanum)
        #compile the regex pattern
        compiledpatt = re.compile(patt)

#        print("patt = {}".format(patt))
        #do the grouping
        groups = defaultdict(list)
        for s in spectrums:
            match = compiledpatt.search(s.idstr)
            if match and match.group(1) and match.group(2):
                groups[match.group(1)].append(s)

        return groups

        
#------------------------------------------------------------------------    
if __name__ == "__main__":
    print("SpectrumRegex.py")