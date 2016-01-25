# -*- coding: utf-8 -*-
"""
Created on Mon May  4 00:48:39 2015

@author: prabu
"""

from __future__ import print_function
import os, os.path
import numpy as np
from SdalReader import SdalReader
from WaveUniquifier import WaveUniquifier

def test(testsdir, verbose = False):
    idir = os.path.join(testsdir, "input")
    edir = os.path.join(testsdir, "expect")
    statuses = []
    
    ifs = ["input_sed_test1.sed", 
           "input_sed_test2.csv",
           "input_sed_test3.sed"]
    ifs = [os.path.join(idir, f) for f in ifs]
    efs = ["expect_sed_test1.sed", 
           "expect_sed_test2.csv",
           "expect_sed_test3.sed"]
    efs = [os.path.join(edir, f) for f in efs]
    
    
    ins = [SdalReader().read_spectrum(f) for f in ifs]
    expuns = [SdalReader().read_spectrum(f) for f in efs]
    uniquifier = WaveUniquifier()
    prouns = [uniquifier.uniquify(s) for s in ins]
    testcount = 0
    for (e, p) in zip(expuns, prouns):
        testcount = testcount + 1
        statuses.append(np.allclose(e.data, p.data, atol = 0.0001))
        statuses.append(e.idstr == p.idstr)
        statuses.append(e.company == p.company)
        statuses.append(e.instrument == p.instrument)
        if not all(statuses):
            print("Failed TEST 1-{}".format(testcount))
    
    #status message
    if all(statuses):
        print("{}: PASSED".format(__file__))
    else:
        print("{}: FAILED".format(__file__))
        
        
if __name__ == "__main__":
    testsdir = "/home/prabu/mycode/sdal/tests_data/test_WaveUniquifier"
    verbose = False
    test(testsdir, verbose)