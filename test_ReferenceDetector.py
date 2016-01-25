# -*- coding: utf-8 -*-
"""
Created on Mon May  4 02:32:57 2015

@author: prabu
"""

from __future__ import print_function
import os, os.path 
from SdalReader import SdalReader
from ReferenceDetector import ReferenceDetector


def test(testsdir, verbose = False):
    idir = os.path.join(testsdir, "input")
    statuses = []
    testcount = 0

    testcount = testcount + 1    
    fs = sorted(os.listdir(idir))
    fps = [os.path.join(idir, f) for f in fs]
    ins = [SdalReader().read_spectrum(f) for f in fps]
    reqdet = [False]*len(ins)
    reqdet[0] = True
    reqdet[12:15] = [True, True, True]
    refdet = ReferenceDetector(context = "gveg")
    det = [refdet.is_reference(s) for s in ins]
    statuses.append(reqdet == det)
    if not all(statuses):
        print("Failed TEST {}".format(testcount))
    
    #status message
    if all(statuses):
        print("{}: PASSED".format(__file__))
    else:
        print("{}: FAILED".format(__file__))


if __name__ == "__main__":
    testsdir = "/home/prabu/mycode/sdal/tests_data/test_ReferenceDetector"
    verbose = False
    test(testsdir, verbose)