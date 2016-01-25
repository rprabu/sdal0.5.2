# -*- coding: utf-8 -*-
"""
Created on Sat May 16 08:50:05 2015

@author: prabu
"""

from __future__ import print_function
import os, os.path
from SdalReader import SdalReader
from SpectrumRegex import SpectrumRegex

def test(testsdir, verbose = False):
    statuses = []
    
    #test 1
    #straightforward grouping with one X
    #glob the files
    idir = os.path.join(testsdir, "test1")
    ifiles = os.listdir(idir)
    ifiles.sort()
    ifiles = [os.path.join(idir, f) for f in ifiles]
    #load the spectrum files
    spectrums = [SdalReader().read_spectrum(f) for f in ifiles]
    #do the regex
    pattern = r'-X'
    groups = SpectrumRegex().make_groups(spectrums, pattern)
    print("pattern = {}".format(pattern))
    for k in groups:
        print("{}:\n\t{}".format(k, "\n\t".join([s.idstr for s in groups[k]])))
    print("\n ---------------- \n")
   
    #test 2
    #grouping with multiple Xs
    #do the regex
    pattern = r'-X-X'
    groups = SpectrumRegex().make_groups(spectrums, pattern)
    print("pattern = {}".format(pattern))
    for k in groups:
        print("{}:\n\t{}".format(k, "\n\t".join([s.idstr for s in groups[k]])))
    print("\n ---------------- \n")
    
    #test 3
    #grouping with multiple Xs same as test 2
    #do the regex
    pattern = r'-X-X-X'
    groups = SpectrumRegex().make_groups(spectrums, pattern)
    print("pattern = {}".format(pattern))
    for k in groups:
        print("{}:\n\t{}".format(k, "\n\t".join([s.idstr for s in groups[k]])))
    print("\n ---------------- \n")
    
    #test 4
    #grouping with multiple Xs same as test 2
    #do the regex
    pattern = r'-X-X-X-X'
    groups = SpectrumRegex().make_groups(spectrums, pattern)
    print("pattern = {}".format(pattern))
    for k in groups:
        print("{}:\n\t{}".format(k, "\n\t".join([s.idstr for s in groups[k]])))

        
    #status message
    if all(statuses):
        print("{}: PASSED".format(__file__))
    else:
        print("{}: FAILED".format(__file__))



if __name__ == "__main__":
    testsdir = "/home/prabu/mycode/sdal/tests_data/test_SpectrumRegex"
    verbose = False
    test(testsdir, verbose)
    

    